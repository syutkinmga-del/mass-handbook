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

  // Все доступные теги (собираются из метаданных статей)
  const allTags = useMemo(() => {
    const tags = new Set<string>();
    
    // Здесь можно добавить логику для получения тегов из статей
    // Пока используем статический список
    const staticTags = [
      'Research',
      'Maritime',
      'Collision Avoidance',
      'Navigation',
      'Dynamic Window Approach',
      'Deep Reinforcement Learning',
      'Path Planning',
      'MASS',
      'COLREGs',
      'Safety',
      'Machine Learning',
      'Sensor Processing',
      'Situational Awareness',
      'Knowledge Representation',
      'Decision Making',
      'Simulation',
      'Real-time',
      'Optimization',
      'Testing',
      'Compliance',
      'IMO',
      'Fuzzy Logic',
      'Genetic Algorithm',
      'Model Predictive Control',
      'Particle Swarm',
      'ASV',
      'USV',
      'Vessel',
    ];
    
    staticTags.forEach(tag => tags.add(tag));
    return Array.from(tags).sort();
  }, []);

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
      
      <div className={styles.tagContainer}>
        {allTags.map((tag) => (
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

      {selectedTags.size > 0 && (
        <div className={styles.selectedTags}>
          <p className={styles.selectedLabel}>Выбранные теги:</p>
          <div className={styles.selectedTagsList}>
            {Array.from(selectedTags).map((tag) => (
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
