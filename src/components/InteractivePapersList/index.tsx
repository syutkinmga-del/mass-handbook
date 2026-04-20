import React, { useState, useMemo, useEffect } from 'react';
import Link from '@docusaurus/Link';
import { papersData } from '@site/src/data/papersData';
import styles from './styles.module.css';

interface Paper {
  id: string;
  title: string;
  tags: string[];
}

const STORAGE_KEY = 'mass-handbook-selected-tags';

/**
 * Интерактивный список статей с фильтрацией по тегам в реальном времени
 */
export default function InteractivePapersList(): JSX.Element {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [isClient, setIsClient] = useState(false);

  // Initialize from localStorage
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

  // Save to localStorage whenever tags change
  useEffect(() => {
    if (isClient) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(selectedTags));
      // Dispatch custom event for sidebar components
      window.dispatchEvent(
        new CustomEvent('tagsChanged', { detail: { tags: selectedTags } })
      );
    }
  }, [selectedTags, isClient]);

  // Filter papers based on selected tags
  const filteredPapers = useMemo(() => {
    if (selectedTags.length === 0) {
      return papersData;
    }

    return papersData.filter(paper =>
      selectedTags.every(tag => paper.tags.includes(tag))
    );
  }, [selectedTags]);

  const toggleTag = (tag: string) => {
    setSelectedTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  const clearTags = () => {
    setSelectedTags([]);
  };

  if (!isClient) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.stats}>
        <p>
          Показано <strong>{filteredPapers.length}</strong> из{' '}
          <strong>{papersData.length}</strong> статей
          {selectedTags.length > 0 && ` (выбрано ${selectedTags.length} тегов)`}
        </p>
      </div>

      {selectedTags.length > 0 && (
        <div className={styles.selectedTags}>
          <div className={styles.tagsLabel}>Выбранные теги:</div>
          <div className={styles.tagsList}>
            {selectedTags.map(tag => (
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
          <button className={styles.clearButton} onClick={clearTags}>
            Очистить все
          </button>
        </div>
      )}

      <div className={styles.papersList}>
        {filteredPapers.length > 0 ? (
          filteredPapers.map((paper, index) => (
            <div key={paper.id} className={styles.paperItem}>
              <div className={styles.paperNumber}>{index + 1}</div>
              <div className={styles.paperContent}>
                <Link to={`/docs/papers/${paper.id}`} className={styles.paperTitle}>
                  {paper.title}
                </Link>
                <div className={styles.paperTags}>
                  {paper.tags.map(tag => (
                    <button
                      key={tag}
                      className={`${styles.tag} ${
                        selectedTags.includes(tag) ? styles.tagSelected : ''
                      }`}
                      onClick={() => toggleTag(tag)}
                      title={`Фильтровать по тегу: ${tag}`}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className={styles.noResults}>
            <p>Статей не найдено с выбранными тегами.</p>
            <button className={styles.clearButton} onClick={clearTags}>
              Очистить фильтр
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
