import React, { ReactNode } from 'react';
import { TagFilterProvider } from '@site/src/contexts/TagFilterContext';
import PaperTagFilter from '@site/src/components/PaperTagFilter';
import styles from './styles.module.css';

interface PaperSectionProps {
  children: ReactNode;
}

/**
 * Компонент-обертка для раздела статей
 * Предоставляет контекст фильтрации и отображает фильтр
 */
export default function PaperSection({ children }: PaperSectionProps): JSX.Element {
  return (
    <TagFilterProvider>
      <div className={styles.paperSection}>
        <PaperTagFilter />
        <div className={styles.paperContent}>
          {children}
        </div>
      </div>
    </TagFilterProvider>
  );
}
