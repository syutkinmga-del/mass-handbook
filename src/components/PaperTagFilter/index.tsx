import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

interface TagCategory {
  name: string;
  tags: string[];
}

const TAG_CATEGORIES: TagCategory[] = [
  {
    name: 'Алгоритмы и модели',
    tags: [
      'Dynamic Window Approach',
      'Deep Reinforcement Learning',
      'Model Predictive Control',
      'Path Planning',
      'Machine Learning',
      'Fuzzy Logic',
      'Genetic Algorithm',
      'Particle Swarm',
      'Reinforcement Learning',
      'Neural Networks',
      'Optimization Algorithm',
    ],
  },
  {
    name: 'Архитектура MASS - Perception',
    tags: ['Perception', 'Sensor Fusion', 'Image Processing'],
  },
  {
    name: 'Архитектура MASS - Decision Making',
    tags: ['Decision Making', 'Behavior Planning', 'Trajectory Planning'],
  },
  {
    name: 'Архитектура MASS - Control',
    tags: ['Control System', 'Adaptive Control', 'Nonlinear Control'],
  },
  {
    name: 'Архитектура MASS - Collision Avoidance',
    tags: ['Collision Avoidance', 'Obstacle Avoidance', 'COLREGs'],
  },
  {
    name: 'Архитектура MASS - Situational Awareness',
    tags: ['Situational Awareness', 'Knowledge Representation', 'Environment Modeling'],
  },
  {
    name: 'Архитектура MASS - Communication & Data Management',
    tags: ['Communication', 'Data Management', 'Cloud Computing'],
  },
  {
    name: 'Архитектура MASS - Human Machine Interaction',
    tags: ['Human Machine Interaction', 'User Interface', 'Remote Control'],
  },
  {
    name: 'Архитектура MASS - Cybersecurity',
    tags: ['Cybersecurity', 'Network Security', 'Data Protection'],
  },
  {
    name: 'Архитектура MASS - System Health Management',
    tags: ['System Health Management', 'Fault Tolerance', 'Maintenance'],
  },
  {
    name: 'Архитектура MASS - Digital Twin Support',
    tags: ['Digital Twin', 'Simulation', 'Testing'],
  },
  {
    name: 'Compliance & Regulatory Layer',
    tags: ['Safety', 'Compliance', 'IMO', 'MASS'],
  },
];

const STORAGE_KEY = 'mass-handbook-selected-tags';

export default function PaperTagFilter(): JSX.Element {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [isClient, setIsClient] = useState(false);

  // Initialize from localStorage on client side
  useEffect(() => {
    setIsClient(true);
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setSelectedTags(JSON.parse(stored));
      } catch (e) {
        console.error('Failed to parse stored tags:', e);
      }
    }
  }, []);

  // Dispatch custom event when tags change so sidebar can listen
  useEffect(() => {
    if (isClient) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(selectedTags));
      // Dispatch custom event for sidebar to listen to
      window.dispatchEvent(
        new CustomEvent('tagsChanged', { detail: { tags: selectedTags } })
      );
    }
  }, [selectedTags, isClient]);

  const toggleTag = (tag: string) => {
    setSelectedTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  const clearTags = () => {
    setSelectedTags([]);
  };

  if (!isClient) {
    return <div className={styles.tagFilter} />;
  }

  return (
    <div className={styles.tagFilter}>
      <div className={styles.header}>
        <h3>Фильтр по тегам</h3>
        {selectedTags.length > 0 && (
          <button className={styles.clearButton} onClick={clearTags}>
            Очистить ({selectedTags.length})
          </button>
        )}
      </div>

      <div className={styles.categoriesContainer}>
        {TAG_CATEGORIES.map(category => (
          <div key={category.name} className={styles.category}>
            <h4 className={styles.categoryTitle}>{category.name}</h4>
            <div className={styles.tagContainer}>
              {category.tags.map(tag => (
                <button
                  key={tag}
                  className={`${styles.tag} ${selectedTags.includes(tag) ? styles.selected : ''}`}
                  onClick={() => toggleTag(tag)}
                  title={`Фильтровать по тегу: ${tag}`}
                >
                  <span className={styles.tagLabel}>{tag}</span>
                  {selectedTags.includes(tag) && <span className={styles.checkmark}>✓</span>}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {selectedTags.length > 0 && (
        <div className={styles.selectedTags}>
          <p className={styles.selectedLabel}>Выбранные теги ({selectedTags.length}):</p>
          <div className={styles.selectedTagsList}>
            {selectedTags.sort().map(tag => (
              <span key={tag} className={styles.selectedTag}>
                {tag}
                <button
                  className={styles.removeTag}
                  onClick={() => toggleTag(tag)}
                  aria-label={`Удалить тег ${tag}`}
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
