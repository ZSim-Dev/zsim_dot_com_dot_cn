<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios';
import { useI18n } from 'vue-i18n';

const { t, locale } = useI18n();

// 投票类别
const voteCategories = computed(() => [
  { key: 'character', label: t('vote.character_vote') },
  { key: 'feature', label: t('vote.feature_vote') },
  { key: 'other', label: t('vote.other_vote') }
]);
const selectedCategoryKey = ref('character');

// 角色投票的临时数据
interface Character {
  id: number
  name: string
  name_en: string
  avatar: string
  votes: number
}

const characters = ref<Character[]>([])
const votedCharacterIds = ref<number[]>([]);
const token = ref(localStorage.getItem('token') || ''); // 从localStorage获取token

async function fetchCharacters() {
  try {
    const response = await axios.get('/api/vote/characters');
    characters.value = response.data;
  } catch (error) {
    console.error('获取角色列表失败:', error);
    // 可以在这里添加用户提示
  }
}

async function fetchUserVotes() {
  if (!token.value) return;
  try {
    const response = await axios.get('/api/vote/user_votes', {
      headers: { Authorization: `Bearer ${token.value}` }
    });
    votedCharacterIds.value = response.data;
  } catch (error) {
    console.error('获取用户投票记录失败:', error);
  }
}

async function handleVote(character: Character) {
  if (!token.value) {
    alert(t('vote.login_to_vote'));
    // 这里可以引导用户去登录页面
    return;
  }

  try {
    await axios.post(`/api/vote/character/${character.id}`, {}, {
      headers: { Authorization: `Bearer ${token.value}` }
    });
    character.votes++;
    votedCharacterIds.value = [...votedCharacterIds.value, character.id];
  } catch (error: any) {
    if (error.response && error.response.data.detail) {
      alert(error.response.data.detail);
    } else {
      console.error('投票失败:', error);
      alert(t('vote.vote_failed'));
    }
  }
}

function switchCategory(categoryKey: string) {
  selectedCategoryKey.value = categoryKey;
}

const getCharacterName = (char: Character) => {
  return locale.value === 'en' ? char.name_en : char.name;
};

const currentCategoryLabel = computed(() => {
    const current = voteCategories.value.find(c => c.key === selectedCategoryKey.value);
    return current ? current.label : '';
});

onMounted(() => {
  fetchCharacters();
  fetchUserVotes();
});
</script>

<template>
  <div class="vote-page">
    <header class="vote-header">
      <h1>{{ t('vote.title') }}</h1>
      <p>{{ t('vote.subtitle') }}</p>
    </header>

    <div class="category-switcher">
      <button v-for="category in voteCategories" :key="category.key" 
        :class="['category-btn', { active: selectedCategoryKey === category.key }]" @click="switchCategory(category.key)">
        {{ category.label }}
      </button>
    </div>

    <div class="vote-content">
      <transition name="fade-view" mode="out-in">
        <div v-if="selectedCategoryKey === 'character'" class="character-grid">
          <div v-for="char in characters" :key="char.id" class="character-card">
            <img :src="char.avatar" :alt="getCharacterName(char)" class="avatar" />
            <span class="name">{{ getCharacterName(char) }}</span>
            <span class="votes">{{ char.votes }} {{ t('vote.votes') }}</span>
            <button class="vote-btn" @click="handleVote(char)" :disabled="votedCharacterIds.includes(char.id)">
              {{ votedCharacterIds.includes(char.id) ? t('vote.voted') : t('vote.vote') }}
            </button>
          </div>
        </div>
        <div v-else class="not-supported">
          <h2>{{ t('vote.not_supported_title', { category: currentCategoryLabel }) }}</h2>
          <p>{{ t('vote.not_supported_text') }}</p>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.vote-page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  animation: fadeInPage 0.5s ease-in-out;
}

@keyframes fadeInPage {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.vote-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.vote-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-heading);
}

.vote-header p {
  font-size: 1.1rem;
  color: var(--color-text);
  margin-top: 0.5rem;
}

.category-switcher {
  display: flex;
  justify-content: center;
  background-color: var(--color-background-mute);
  border-radius: 12px;
  padding: 5px;
  margin-bottom: 2.5rem;
}

.category-btn {
  flex: 1;
  padding: 10px 20px;
  border: none;
  background-color: transparent;
  color: var(--color-text);
  font-size: 1rem;
  font-weight: 500;
  border-radius: 9px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-btn.active {
  background-color: var(--color-background);
  color: var(--color-heading);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.vote-content {
  min-height: 400px;
}

.character-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  max-width: 100%;
}

@media (min-width: 768px) {
  .character-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
}

@media (min-width: 1024px) {
  .character-grid {
    grid-template-columns: repeat(auto-fit, minmax(240px, 300px));
    justify-content: center;
  }
}

@media (min-width: 1200px) {
  .character-grid {
    grid-template-columns: repeat(auto-fit, minmax(260px, 320px));
  }
}

.character-card {
  background: var(--color-background-soft);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.character-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
  border: 3px solid var(--color-background);
}

.name {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-heading);
}

.votes {
  font-size: 0.9rem;
  color: var(--color-text);
  margin: 0.25rem 0 1rem 0;
}

.vote-btn {
  width: 100%;
  padding: 10px;
  border: none;
  background-color: var(--vt-c-indigo);
  color: white;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.vote-btn:hover {
  background-color: #3c4a5c;
}

.vote-btn:active {
  transform: scale(0.95);
}

.vote-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.not-supported {
  text-align: center;
  padding: 4rem 1rem;
  background-color: var(--color-background-soft);
  border-radius: 16px;
}

.not-supported h2 {
  font-size: 1.8rem;
  color: var(--color-heading);
}

.not-supported p {
  font-size: 1.1rem;
  color: var(--color-text);
  margin-top: 1rem;
}

.fade-view-enter-active,
.fade-view-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-view-enter-from,
.fade-view-leave-to {
  opacity: 0;
  transform: translateY(15px);
}
</style>