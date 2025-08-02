import datetime
from typing import Any

import httpx
from pydantic import BaseModel

# --- Configuration ---
REPO_OWNER = "ZSim-Dev"
REPO_NAME = "ZSim"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"


# --- In-memory Cache ---
class LatestReleaseCache(BaseModel):
    version: str
    download_url: str | None
    release_page_url: str | None
    available: bool
    expired_at: int


_latest_release_cache: LatestReleaseCache = LatestReleaseCache(
    version="N/A",
    download_url=None,  # URL for the stable build asset
    release_page_url=None,  # URL to the GitHub releases page
    available=False,
    expired_at=0,
)


# --- Core Logic ---
async def _fetch_and_update_cache():
    """
    Fetches the latest release from GitHub and updates the cache.
    The 'stable' version is the one marked as 'latest' on GitHub,
    is not a pre-release, and has a valid Windows .zip asset.
    """
    global _latest_release_cache
    expired_at = _latest_release_cache.expired_at
    time_stamp_now = int(datetime.datetime.now().timestamp())
    if expired_at > 0 and expired_at > time_stamp_now:
        return
    try:
        print("[GitHub] Fetching latest release...")
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(API_URL)
            response.raise_for_status()
            data: dict[str, Any] = response.json()

        is_prerelease = data.get("prerelease", False)

        asset_url = None
        for asset in data.get("assets", []):
            if "windows" in asset.get("name", "").lower() and asset.get("name", "").endswith(".zip"):
                asset_url = asset.get("browser_download_url")
                break

        if not is_prerelease:
            _latest_release_cache = LatestReleaseCache(
                version=data.get("tag_name", "N/A"),
                download_url=asset_url,
                release_page_url=data.get("html_url"),
                available=True,
                expired_at=time_stamp_now + 60,
            )
            print(f"[GitHub] Cache updated. Latest stable release: {data.get('tag_name')}")
        else:
            _latest_release_cache.available = False
            reason = "it's a pre-release" if is_prerelease else "no suitable download asset found"
            print(f"[GitHub] No stable release available. Reason: {reason}.")

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print("[GitHub] No 'latest' release found for the repository.")
        else:
            print(f"[GitHub] HTTP error fetching latest release: {e}")
        _latest_release_cache.available = False
    except Exception as e:
        print(f"[GitHub] An unexpected error occurred while fetching release: {e}")
        _latest_release_cache.available = False


async def get_latest_release_from_cache() -> LatestReleaseCache:
    """Provides the currently cached latest release information."""
    await _fetch_and_update_cache()
    print(f"[GitHub] Returning cached release: {_latest_release_cache}")
    return _latest_release_cache
