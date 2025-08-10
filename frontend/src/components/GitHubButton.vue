<template>
  <button class="github-btn" @click="openGitHub">
    <svg t="1717920000000" class="github-icon" viewBox="0 0 1024 1024" width="24" height="24">
      <path
        d="M511.6 76.3C264.6 76.3 64 277.5 64 525.2c0 198.1 128.5 366.2 306.7 425.8 22.4 4.1 30.6-9.7 30.6-21.5 0-10.6-0.4-45.5-0.6-82.5-124.8 27.1-151.2-60.2-151.2-60.2-20.4-51.8-49.8-65.6-49.8-65.6-40.7-27.8 3.1-27.2 3.1-27.2 45 3.2 68.7 46.2 68.7 46.2 40 68.6 104.9 48.8 130.5 37.3 4.1-29 15.7-48.8 28.6-60-99.7-11.3-204.5-49.8-204.5-221.8 0-49 17.5-89 46.2-120.4-4.6-11.3-20-56.8 4.4-118.5 0 0 37.6-12.1 123.2 46.1 35.7-9.9 74-14.8 112.1-15 38 0.2 76.4 5.1 112.1 15 85.5-58.2 123.1-46.1 123.1-46.1 24.5 61.7 9.1 107.2 4.5 118.5 28.8 31.4 46.1 71.4 46.1 120.4 0 172.4-104.9 210.4-204.9 221.5 16.1 13.9 30.4 41.3 30.4 83.3 0 60.2-0.5 108.7-0.5 123.5 0 11.9 8 25.8 30.7 21.4C831.6 891.2 960 723.2 960 525.2c0-247.7-200.6-448.9-448.4-448.9z"
        fill="currentColor"
      />
    </svg>
  </button>
</template>

<script setup lang="ts">
  interface Props {
    url?: string
  }

  const props = withDefaults(defineProps<Props>(), {
    url: 'https://github.com/ZZZSimulator/ZSim',
  })

  function openGitHub() {
    window.open(props.url, '_blank')
  }
</script>

<style scoped>
  .github-btn {
    background: none;
    border: none;
    cursor: pointer;
    border-radius: 50%;
    padding: 4px;
    transition: background 0.3s ease;
    color: var(--github-fill);
  }

  .github-btn:hover {
    background: var(--hover-bg);
  }

  .github-icon {
    display: block;
  }
</style>
