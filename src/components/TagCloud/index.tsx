import React, { useMemo } from 'react';
import styles from './styles.module.css';

interface TagCloudProps {
  onTagClick?: (tag: string) => void;
  maxTags?: number;
}

interface TagWithSize {
  tag: string;
  count: number;
  size: number;
  frequency: number;
}

export default function TagCloud({ onTagClick, maxTags = 30 }: TagCloudProps) {
  const tagsData = useMemo(() => {
    // Tag frequency data from papers
    const tagFrequency: Record<string, number> = {
      'Collision Avoidance': 10,
      'MASS': 8,
      'Decision Making': 7,
      'Genetic Algorithm': 7,
      'User Interface': 6,
      'Dynamic Window Approach': 5,
      'Path Planning': 4,
      'Knowledge Representation': 4,
      'Compliance': 3,
      'Trajectory Planning': 3,
      'Obstacle Avoidance': 3,
      'Safety': 2,
      'Deep Reinforcement Learning': 2,
      'Reinforcement Learning': 2,
      'Situational Awareness': 2,
      'Perception': 2,
      'COLREGs': 1,
      'Fuzzy Logic': 1,
      'Digital Twin': 1,
      'Simulation': 1,
      'Fault Tolerance': 1,
      'Optimization Algorithm': 1,
      'Testing': 1,
    };

    // Get top tags
    const topTags = Object.entries(tagFrequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, maxTags)
      .map(([tag, count]) => ({ tag, count }));

    // Calculate min and max for size scaling
    const counts = topTags.map(t => t.count);
    const minCount = Math.min(...counts);
    const maxCount = Math.max(...counts);
    const range = maxCount - minCount || 1;

    // Map counts to sizes (1-5 scale)
    const tagsWithSize: TagWithSize[] = topTags.map(({ tag, count }) => {
      const frequency = (count - minCount) / range;
      const size = 1 + frequency * 4; // Size from 1 to 5
      return { tag, count, size, frequency };
    });

    // Shuffle for better visual distribution
    return tagsWithSize.sort(() => Math.random() - 0.5);
  }, [maxTags]);

  const handleTagClick = (tag: string) => {
    if (onTagClick) {
      onTagClick(tag);
    }
    // Dispatch custom event for filter synchronization
    const event = new CustomEvent('tagsChanged', { detail: { selectedTags: [tag] } });
    window.dispatchEvent(event);
  };

  return (
    <div className={styles.tagCloudContainer}>
      <h2 className={styles.title}>Облако тегов</h2>
      <p className={styles.description}>
        Популярные теги из базы статей. Нажмите на тег для фильтрации статей.
      </p>
      <div className={styles.cloudWrapper}>
        {tagsData.map(({ tag, count, size }) => (
          <button
            key={tag}
            className={`${styles.tag} ${styles[`size${Math.round(size)}`]}`}
            onClick={() => handleTagClick(tag)}
            title={`${count} статей`}
            aria-label={`${tag} (${count} статей)`}
          >
            <span className={styles.tagText}>{tag}</span>
            <span className={styles.tagCount}>{count}</span>
          </button>
        ))}
      </div>
      <div className={styles.legend}>
        <p className={styles.legendText}>
          <strong>Размер</strong> указывает на популярность тега среди статей
        </p>
      </div>
    </div>
  );
}
