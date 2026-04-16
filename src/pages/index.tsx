import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/papers">
            Перейти к статьям 📚
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/glossary"
            style={{marginLeft: '10px'}}>
            Глоссарий 📖
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({title, description, icon}: {title: string; description: string; icon: string}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center" style={{fontSize: '48px', marginBottom: '16px'}}>
        {icon}
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} - Справочник для разработчиков MASS`}
      description="Интерактивный справочник для разработчиков автономных морских судов с научными статьями, гайдами и алгоритмами">
      <HomepageHeader />
      <main>
        <section className={styles.features} style={{padding: '40px 0'}}>
          <div className="container">
            <Heading as="h2" style={{textAlign: 'center', marginBottom: '40px'}}>
              Основные возможности
            </Heading>
            <div className="row">
              <FeatureCard
                icon="📚"
                title="База научных статей"
                description="Автоматически пополняемая коллекция релевантных публикаций из мировых баз данных (CrossRef, arXiv). Все статьи аннотированы и содержат ключевые выводы для практического применения."
              />
              <FeatureCard
                icon="🛠️"
                title="Практические гайды"
                description="Руководства по реализации алгоритмов навигации, систем предотвращения столкновений и интеграции с бортовыми сенсорами."
              />
              <FeatureCard
                icon="📖"
                title="Глоссарий терминов"
                description="Единый словарь специфических терминов, аббревиатур и понятий из области MASS и морской навигации."
              />
            </div>
          </div>
        </section>

        <section style={{backgroundColor: '#f5f5f5', padding: '40px 0'}}>
          <div className="container">
            <Heading as="h2" style={{textAlign: 'center', marginBottom: '20px'}}>
              О справочнике
            </Heading>
            <p style={{textAlign: 'center', maxWidth: '800px', margin: '0 auto', lineHeight: '1.6'}}>
              <strong>MASS Handbook</strong> создан специально для инженеров, исследователей и разработчиков, 
              работающих над технологиями автономного судовождения. Здесь собраны передовые научные статьи, 
              практические гайды и глоссарий терминов, которые помогут вам в проектировании надежных и безопасных 
              систем для морских автономных надводных судов (Maritime Autonomous Surface Ships).
            </p>
            <p style={{textAlign: 'center', marginTop: '20px'}}>
              Справочник демонстрирует передовые подходы к автоматизации: автоматический сбор статей из научных баз, 
              интеллектуальная обработка контента с использованием LLM, и непрерывная интеграция через CI/CD пайплайн.
            </p>
          </div>
        </section>

        <section style={{padding: '40px 0'}}>
          <div className="container">
            <Heading as="h2" style={{textAlign: 'center', marginBottom: '30px'}}>
              Начните с этого
            </Heading>
            <div className="row" style={{justifyContent: 'center'}}>
              <div className={clsx('col col--4')} style={{marginBottom: '20px'}}>
                <div className={clsx('card', styles.card)}>
                  <div className="card__header">
                    <Heading as="h3">Новичок?</Heading>
                  </div>
                  <div className="card__body">
                    <p>Начните с введения и изучите основные концепции MASS.</p>
                  </div>
                  <div className="card__footer">
                    <Link className="button button--primary button--block" to="/docs/intro">
                      Введение
                    </Link>
                  </div>
                </div>
              </div>
              <div className={clsx('col col--4')} style={{marginBottom: '20px'}}>
                <div className={clsx('card', styles.card)}>
                  <div className="card__header">
                    <Heading as="h3">Ищете статьи?</Heading>
                  </div>
                  <div className="card__body">
                    <p>Просмотрите нашу базу научных публикаций по избежанию столкновений и навигации.</p>
                  </div>
                  <div className="card__footer">
                    <Link className="button button--primary button--block" to="/docs/papers">
                      Статьи
                    </Link>
                  </div>
                </div>
              </div>
              <div className={clsx('col col--4')} style={{marginBottom: '20px'}}>
                <div className={clsx('card', styles.card)}>
                  <div className="card__header">
                    <Heading as="h3">Нужен глоссарий?</Heading>
                  </div>
                  <div className="card__body">
                    <p>Найдите определения ключевых терминов и аббревиатур MASS.</p>
                  </div>
                  <div className="card__footer">
                    <Link className="button button--primary button--block" to="/docs/glossary">
                      Глоссарий
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
