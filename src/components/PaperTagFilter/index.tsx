import React, { useState, useMemo } from 'react';
import styles from './styles.module.css';

interface PaperTagFilterProps {
  onTagsChange?: (selectedTags: string[]) => void;
}

/**
 * Компонент для фильтрации статей по тегам
 * Отображает все доступные теги и позволяет выбирать несколько тегов одновременно
 */
export default function PaperTagFilter({ onTagsChange }: PaperTagFilterProps): JSX.Element {
  const [selectedTags, setSelectedTags] = useState<Set<string>>(new Set());

  // Все доступные теги, организованные по категориям
  const tagCategories = useMemo(() => ({
    'Алгоритмы и модели': [
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
    'Архитектура MASS - Perception': [
      'Perception',
      'Sensor Fusion',
      'Image Processing',
    ],
    'Архитектура MASS - Decision Making': [
      'Decision Making',
      'Behavior Planning',
      'Trajectory Planning',
    ],
    'Архитектура MASS - Control': [
      'Control System',
      'Adaptive Control',
      'Nonlinear Control',
    ],
    'Архитектура MASS - Collision Avoidance': [
      'Collision Avoidance',
      'Obstacle Avoidance',
      'COLREGs',
    ],
    'Архитектура MASS - Situational Awareness': [
      'Situational Awareness',
      'Knowledge Representation',
      'Environment Modeling',
    ],
    'Архитектура MASS - Communication & Data Management': [
      'Communication',
      'Data Management',
      'Cloud Computing',
    ],
    'Архитектура MASS - Human Machine Interaction': [
      'Human Machine Interaction',
      'User Interface',
      'Remote Control',
    ],
    'Архитектура MASS - Cybersecurity': [
      'Cybersecurity',
      'Network Security',
      'Data Protection',
    ],
    'Архитектура MASS - System Health Management': [
      'System Health Management',
      'Fault Tolerance',
      'Maintenance',
    ],
    'Архитектура MASS - Digital Twin Support': [
      'Digital Twin',
      'Simulation',
      'Testing',
    ],
    'Compliance & Regulatory Layer': [
      'Safety',
      'Compliance',
      'IMO',
      'MASS',
    ],
  }), []);

  const allTags = useMemo(() => {
    return Object.values(tagCategories).flat().sort();
  }, [tagCategories]);

  const handleTagToggle = (tag: string) => {
    const newSelectedTags = new Set(selectedTags);
    if (newSelectedTags.has(tag)) {
      newSelectedTags.delete(tag);
    } else {
      newSelectedTags.add(tag);
    }
    setSelectedTags(newSelectedTags);
    onTagsChange?.(Array.from(newSelectedTags));
  };

  const handleClearAll = () => {
    setSelectedTags(new Set());
    onTagsChange?.([]);
  };

  return (
    <div className={styles.tagFilter}>
      <div className={styles.header}>
        <h3>Фильтр по тегам</h3>
        {selectedTags.size > 0 && (
          <button className={styles.clearButton} onClick={handleClearAll}>
            Очистить ({selectedTags.size})
          </button>
        )}
      </div>
      
      <div className={styles.categoriesContainer}>
        {Object.entries(tagCategories).map(([category, tags]) => (
          <div key={category} className={styles.category}>
            <h4 className={styles.categoryTitle}>{category}</h4>
            <div className={styles.tagContainer}>
              {tags.map((tag) => (
                <button
                  key={tag}
                  className={`${styles.tag} ${selectedTags.has(tag) ? styles.selected : ''}`}
                  onClick={() => handleTagToggle(tag)}
                  title={`Фильтровать по тегу: ${tag}`}
                >
                  <span className={styles.tagLabel}>{tag}</span>
                  {selectedTags.has(tag) && <span className={styles.checkmark}>✓</span>}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {selectedTags.size > 0 && (
        <div className={styles.selectedTags}>
          <p className={styles.selectedLabel}>Выбранные теги ({selectedTags.size}):</p>
          <div className={styles.selectedTagsList}>
            {Array.from(selectedTags).sort().map((tag) => (
              <span key={tag} className={styles.selectedTag}>
                {tag}
                <button
                  className={styles.removeTag}
                  onClick={() => handleTagToggle(tag)}
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
