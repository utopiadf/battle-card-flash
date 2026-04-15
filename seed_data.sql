-- ============================================================
-- Seed Data for Battle Card Flash
-- ============================================================

-- Products
INSERT INTO products (name, vendor, description, is_default) VALUES
('TiDB', 'PingCAP', 'Distributed SQL database with MySQL compatibility, HTAP capabilities, and horizontal scalability', 1),
('MySQL', 'Oracle', 'Popular open-source relational database with broad ecosystem support', 0),
('PostgreSQL', 'PostgreSQL Global Dev Group', 'Advanced open-source relational database with extensibility and standards compliance', 0),
('CockroachDB', 'Cockroach Labs', 'Distributed SQL database designed for cloud-native resilience and global scale', 0),
('Amazon Aurora', 'AWS', 'Cloud-native relational database with MySQL and PostgreSQL compatibility', 0),
('Google Spanner', 'Google Cloud', 'Globally distributed, strongly consistent database service', 0),
('MongoDB', 'MongoDB Inc.', 'Document-oriented NoSQL database for flexible schema workloads', 0),
('PlanetScale', 'PlanetScale', 'MySQL-compatible serverless database platform built on Vitess', 0),
('SingleStore', 'SingleStore', 'Distributed SQL database optimized for real-time analytics and transactions', 0),
('OceanBase', 'Ant Group', 'Distributed relational database for enterprise-grade financial workloads', 0);

-- Industries
INSERT INTO industries (name, description, icon_name, sort_order) VALUES
('AI', 'AI agent applications requiring vector search, RAG pipelines, and real-time inference', 'PSYCHOLOGY', 1),
('Gaming', 'Online gaming backends needing low latency, high throughput, and global distribution', 'SPORTS_ESPORTS', 2),
('eCommerce', 'E-commerce platforms requiring ACID transactions, inventory management, and analytics', 'SHOPPING_CART', 3),
('Fintech', 'Financial systems demanding strong consistency, compliance, and high availability', 'ACCOUNT_BALANCE', 4),
('SaaS', 'Multi-tenant SaaS applications needing tenant isolation and elastic scaling', 'CLOUD', 5),
('Retail', 'Retail systems requiring real-time inventory, POS integration, omnichannel analytics, and supply chain management', 'STOREFRONT', 6);

-- Features (across categories)
INSERT INTO features (name, category, description, data_type) VALUES
-- Scalability
('Horizontal Scaling', 'Scalability', 'Ability to scale out by adding nodes', 'text'),
('Auto-Sharding', 'Scalability', 'Automatic data distribution across nodes', 'text'),
('Max Cluster Size', 'Scalability', 'Maximum supported cluster node count', 'text'),
('Elastic Scaling', 'Scalability', 'Dynamic scale up/down without downtime', 'text'),
-- SQL Compatibility
('MySQL Compatibility', 'SQL Compatibility', 'Level of MySQL protocol and syntax support', 'text'),
('PostgreSQL Compatibility', 'SQL Compatibility', 'Level of PostgreSQL protocol and syntax support', 'text'),
('Distributed SQL', 'SQL Compatibility', 'Full SQL support across distributed nodes', 'text'),
('ACID Transactions', 'SQL Compatibility', 'Distributed ACID transaction support', 'text'),
-- Performance
('Read Latency (p99)', 'Performance', 'Typical p99 read latency', 'text'),
('Write Throughput', 'Performance', 'Sustained write operations per second', 'text'),
('HTAP Capability', 'Performance', 'Hybrid transactional and analytical processing', 'text'),
('Query Optimizer', 'Performance', 'Sophistication of the query optimizer', 'text'),
-- AI/ML
('Vector Search', 'AI/ML', 'Native vector similarity search support', 'text'),
('JSON/Document Support', 'AI/ML', 'JSON storage and querying capabilities', 'text'),
('Change Data Capture', 'AI/ML', 'Real-time change data capture for streaming', 'text'),
('ML Integration', 'AI/ML', 'Integration with ML frameworks and pipelines', 'text'),
-- Operations
('Managed Service', 'Operations', 'Fully managed cloud service availability', 'text'),
('Kubernetes Native', 'Operations', 'Native Kubernetes operator and deployment', 'text'),
('Backup & Restore', 'Operations', 'Backup and point-in-time recovery capabilities', 'text'),
('Monitoring & Observability', 'Operations', 'Built-in monitoring dashboards and metrics', 'text'),
-- Cost
('Pricing Model', 'Cost', 'Pricing structure and model', 'text'),
('Free Tier', 'Cost', 'Availability and limits of free tier', 'text'),
('TCO at Scale', 'Cost', 'Total cost of ownership at large scale', 'text'),
-- Reliability
('RPO/RTO', 'Reliability', 'Recovery point and recovery time objectives', 'text'),
('Multi-Region', 'Reliability', 'Multi-region deployment and replication', 'text'),
('Automatic Failover', 'Reliability', 'Automatic failure detection and recovery', 'text'),
('Data Encryption', 'Reliability', 'Encryption at rest and in transit', 'text');

-- PLACEHOLDER_INDUSTRY_FEATURES

-- Industry-Feature Mappings
-- AI Agent industry
INSERT INTO industry_features (industry_id, feature_id, weight, sort_order)
SELECT s.id, f.id, m.weight, m.sort_order FROM industries s,
(SELECT 'Vector Search' AS fname, 'AI/ML' AS fcat, 2.0 AS weight, 1 AS sort_order
 UNION ALL SELECT 'JSON/Document Support', 'AI/ML', 1.5, 2
 UNION ALL SELECT 'Read Latency (p99)', 'Performance', 1.5, 3
 UNION ALL SELECT 'Horizontal Scaling', 'Scalability', 1.2, 4
 UNION ALL SELECT 'HTAP Capability', 'Performance', 1.3, 5
 UNION ALL SELECT 'Change Data Capture', 'AI/ML', 1.0, 6
 UNION ALL SELECT 'ML Integration', 'AI/ML', 1.0, 7
 UNION ALL SELECT 'Managed Service', 'Operations', 0.8, 8
 UNION ALL SELECT 'Elastic Scaling', 'Scalability', 0.8, 9
 UNION ALL SELECT 'Pricing Model', 'Cost', 0.7, 10
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE s.name = 'AI';

-- Gaming industry
INSERT INTO industry_features (industry_id, feature_id, weight, sort_order)
SELECT s.id, f.id, m.weight, m.sort_order FROM industries s,
(SELECT 'Read Latency (p99)' AS fname, 'Performance' AS fcat, 2.0 AS weight, 1 AS sort_order
 UNION ALL SELECT 'Write Throughput', 'Performance', 2.0, 2
 UNION ALL SELECT 'Multi-Region', 'Reliability', 1.5, 3
 UNION ALL SELECT 'Automatic Failover', 'Reliability', 1.5, 4
 UNION ALL SELECT 'Horizontal Scaling', 'Scalability', 1.3, 5
 UNION ALL SELECT 'ACID Transactions', 'SQL Compatibility', 1.0, 6
 UNION ALL SELECT 'Elastic Scaling', 'Scalability', 1.0, 7
 UNION ALL SELECT 'Managed Service', 'Operations', 0.8, 8
 UNION ALL SELECT 'TCO at Scale', 'Cost', 0.8, 9
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE s.name = 'Gaming';

-- E-Commerce industry
INSERT INTO industry_features (industry_id, feature_id, weight, sort_order)
SELECT s.id, f.id, m.weight, m.sort_order FROM industries s,
(SELECT 'ACID Transactions' AS fname, 'SQL Compatibility' AS fcat, 2.0 AS weight, 1 AS sort_order
 UNION ALL SELECT 'MySQL Compatibility', 'SQL Compatibility', 1.5, 2
 UNION ALL SELECT 'HTAP Capability', 'Performance', 1.5, 3
 UNION ALL SELECT 'Horizontal Scaling', 'Scalability', 1.3, 4
 UNION ALL SELECT 'Read Latency (p99)', 'Performance', 1.2, 5
 UNION ALL SELECT 'Write Throughput', 'Performance', 1.2, 6
 UNION ALL SELECT 'Automatic Failover', 'Reliability', 1.0, 7
 UNION ALL SELECT 'Backup & Restore', 'Operations', 0.8, 8
 UNION ALL SELECT 'Data Encryption', 'Reliability', 0.8, 9
 UNION ALL SELECT 'Pricing Model', 'Cost', 0.7, 10
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE s.name = 'eCommerce';

-- Financial Services industry
INSERT INTO industry_features (industry_id, feature_id, weight, sort_order)
SELECT s.id, f.id, m.weight, m.sort_order FROM industries s,
(SELECT 'ACID Transactions' AS fname, 'SQL Compatibility' AS fcat, 2.0 AS weight, 1 AS sort_order
 UNION ALL SELECT 'RPO/RTO', 'Reliability', 2.0, 2
 UNION ALL SELECT 'Data Encryption', 'Reliability', 1.8, 3
 UNION ALL SELECT 'Multi-Region', 'Reliability', 1.5, 4
 UNION ALL SELECT 'Automatic Failover', 'Reliability', 1.5, 5
 UNION ALL SELECT 'MySQL Compatibility', 'SQL Compatibility', 1.0, 6
 UNION ALL SELECT 'Backup & Restore', 'Operations', 1.0, 7
 UNION ALL SELECT 'Monitoring & Observability', 'Operations', 0.8, 8
 UNION ALL SELECT 'Horizontal Scaling', 'Scalability', 0.8, 9
 UNION ALL SELECT 'Query Optimizer', 'Performance', 0.7, 10
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE s.name = 'Fintech';

-- PLACEHOLDER_PRODUCT_FEATURES

-- SaaS Multi-Tenant industry
INSERT INTO industry_features (industry_id, feature_id, weight, sort_order)
SELECT s.id, f.id, m.weight, m.sort_order FROM industries s,
(SELECT 'Horizontal Scaling' AS fname, 'Scalability' AS fcat, 2.0 AS weight, 1 AS sort_order
 UNION ALL SELECT 'Elastic Scaling', 'Scalability', 1.8, 2
 UNION ALL SELECT 'MySQL Compatibility', 'SQL Compatibility', 1.3, 3
 UNION ALL SELECT 'ACID Transactions', 'SQL Compatibility', 1.2, 4
 UNION ALL SELECT 'Managed Service', 'Operations', 1.2, 5
 UNION ALL SELECT 'Monitoring & Observability', 'Operations', 1.0, 6
 UNION ALL SELECT 'TCO at Scale', 'Cost', 1.0, 7
 UNION ALL SELECT 'Pricing Model', 'Cost', 0.8, 8
 UNION ALL SELECT 'Multi-Region', 'Reliability', 0.8, 9
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE s.name = 'SaaS';

-- Retail industry
INSERT INTO industry_features (industry_id, feature_id, weight, sort_order)
SELECT s.id, f.id, m.weight, m.sort_order FROM industries s,
(SELECT 'ACID Transactions' AS fname, 'SQL Compatibility' AS fcat, 2.0 AS weight, 1 AS sort_order
 UNION ALL SELECT 'Read Latency (p99)', 'Performance', 1.8, 2
 UNION ALL SELECT 'Write Throughput', 'Performance', 1.5, 3
 UNION ALL SELECT 'Horizontal Scaling', 'Scalability', 1.5, 4
 UNION ALL SELECT 'HTAP Capability', 'Performance', 1.3, 5
 UNION ALL SELECT 'Multi-Region', 'Reliability', 1.2, 6
 UNION ALL SELECT 'Automatic Failover', 'Reliability', 1.0, 7
 UNION ALL SELECT 'MySQL Compatibility', 'SQL Compatibility', 1.0, 8
 UNION ALL SELECT 'Backup & Restore', 'Operations', 0.8, 9
 UNION ALL SELECT 'TCO at Scale', 'Cost', 0.8, 10
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE s.name = 'Retail';

-- ============================================================
-- Product Feature Values
-- ============================================================

-- TiDB feature values
INSERT INTO product_features (product_id, feature_id, value, source)
SELECT p.id, f.id, m.val, m.src FROM products p,
(SELECT 'Horizontal Scaling' AS fname, 'Scalability' AS fcat, 'Native horizontal scaling via TiKV storage layer' AS val, 'official_docs' AS src
 UNION ALL SELECT 'Auto-Sharding', 'Scalability', 'Automatic Region-based sharding with dynamic splitting', 'official_docs'
 UNION ALL SELECT 'Max Cluster Size', 'Scalability', '500+ nodes in production deployments', 'benchmark'
 UNION ALL SELECT 'Elastic Scaling', 'Scalability', 'Online scaling without downtime via TiDB Operator', 'official_docs'
 UNION ALL SELECT 'MySQL Compatibility', 'SQL Compatibility', 'High - MySQL 5.7/8.0 protocol compatible', 'official_docs'
 UNION ALL SELECT 'PostgreSQL Compatibility', 'SQL Compatibility', 'Not supported', 'official_docs'
 UNION ALL SELECT 'Distributed SQL', 'SQL Compatibility', 'Full distributed SQL with cross-node joins', 'official_docs'
 UNION ALL SELECT 'ACID Transactions', 'SQL Compatibility', 'Distributed ACID with Percolator-based 2PC', 'official_docs'
 UNION ALL SELECT 'Read Latency (p99)', 'Performance', '< 10ms for point queries', 'benchmark'
 UNION ALL SELECT 'Write Throughput', 'Performance', '100K+ TPS with horizontal scaling', 'benchmark'
 UNION ALL SELECT 'HTAP Capability', 'Performance', 'Native HTAP via TiFlash columnar engine', 'official_docs'
 UNION ALL SELECT 'Query Optimizer', 'Performance', 'Cost-based optimizer with statistics collection', 'official_docs'
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE p.name = 'TiDB';

-- TiDB AI/ML + Operations + Cost + Reliability
INSERT INTO product_features (product_id, feature_id, value, source)
SELECT p.id, f.id, m.val, m.src FROM products p,
(SELECT 'Vector Search' AS fname, 'AI/ML' AS fcat, 'Supported via TiDB Vector (built-in vector data type)' AS val, 'official_docs' AS src
 UNION ALL SELECT 'JSON/Document Support', 'AI/ML', 'Full JSON data type with indexing support', 'official_docs'
 UNION ALL SELECT 'Change Data Capture', 'AI/ML', 'TiCDC for real-time change streaming to Kafka/MySQL', 'official_docs'
 UNION ALL SELECT 'ML Integration', 'AI/ML', 'Integration with AI frameworks via TiDB Vector and CDC', 'official_docs'
 UNION ALL SELECT 'Managed Service', 'Operations', 'TiDB Cloud (fully managed) on AWS and GCP', 'official_docs'
 UNION ALL SELECT 'Kubernetes Native', 'Operations', 'TiDB Operator for native K8s deployment', 'official_docs'
 UNION ALL SELECT 'Backup & Restore', 'Operations', 'BR tool for full/incremental backup, PITR supported', 'official_docs'
 UNION ALL SELECT 'Monitoring & Observability', 'Operations', 'TiDB Dashboard, Grafana, Prometheus integration', 'official_docs'
 UNION ALL SELECT 'Pricing Model', 'Cost', 'Open source (self-hosted free), TiDB Cloud pay-as-you-go', 'official_docs'
 UNION ALL SELECT 'Free Tier', 'Cost', 'TiDB Cloud Serverless free tier (25 GiB storage)', 'official_docs'
 UNION ALL SELECT 'TCO at Scale', 'Cost', 'Competitive - open source + efficient resource utilization', 'expert'
 UNION ALL SELECT 'RPO/RTO', 'Reliability', 'RPO=0 (sync replication), RTO < 30s', 'official_docs'
 UNION ALL SELECT 'Multi-Region', 'Reliability', 'Multi-region deployment with Placement Rules', 'official_docs'
 UNION ALL SELECT 'Automatic Failover', 'Reliability', 'Automatic leader election via Raft consensus', 'official_docs'
 UNION ALL SELECT 'Data Encryption', 'Reliability', 'TLS in transit, AES-256 at rest', 'official_docs'
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE p.name = 'TiDB';

-- PLACEHOLDER_MYSQL_FEATURES

-- MySQL feature values
INSERT INTO product_features (product_id, feature_id, value, source)
SELECT p.id, f.id, m.val, m.src FROM products p,
(SELECT 'Horizontal Scaling' AS fname, 'Scalability' AS fcat, 'Limited - requires manual sharding or middleware (Vitess, ProxySQL)' AS val, 'official_docs' AS src
 UNION ALL SELECT 'Auto-Sharding', 'Scalability', 'Not native - requires external solutions', 'official_docs'
 UNION ALL SELECT 'Max Cluster Size', 'Scalability', 'Single node primary; InnoDB Cluster up to 9 nodes', 'official_docs'
 UNION ALL SELECT 'Elastic Scaling', 'Scalability', 'Vertical scaling; read replicas for read scaling', 'official_docs'
 UNION ALL SELECT 'MySQL Compatibility', 'SQL Compatibility', 'Native - the reference implementation', 'official_docs'
 UNION ALL SELECT 'PostgreSQL Compatibility', 'SQL Compatibility', 'Not supported', 'official_docs'
 UNION ALL SELECT 'Distributed SQL', 'SQL Compatibility', 'Not supported natively', 'official_docs'
 UNION ALL SELECT 'ACID Transactions', 'SQL Compatibility', 'Full ACID with InnoDB (single node)', 'official_docs'
 UNION ALL SELECT 'Read Latency (p99)', 'Performance', '< 5ms for point queries (single node)', 'benchmark'
 UNION ALL SELECT 'Write Throughput', 'Performance', '10K-50K TPS (single node, hardware dependent)', 'benchmark'
 UNION ALL SELECT 'HTAP Capability', 'Performance', 'Limited - HeatWave for analytics (Oracle Cloud only)', 'official_docs'
 UNION ALL SELECT 'Query Optimizer', 'Performance', 'Cost-based optimizer, mature and well-tested', 'official_docs'
 UNION ALL SELECT 'Vector Search', 'AI/ML', 'MySQL 9.0+ vector data type (limited)', 'official_docs'
 UNION ALL SELECT 'JSON/Document Support', 'AI/ML', 'JSON data type with path-based queries', 'official_docs'
 UNION ALL SELECT 'Change Data Capture', 'AI/ML', 'Binary log replication, Debezium connector', 'official_docs'
 UNION ALL SELECT 'ML Integration', 'AI/ML', 'Limited native support; external tools required', 'expert'
 UNION ALL SELECT 'Managed Service', 'Operations', 'RDS MySQL, Azure MySQL, Cloud SQL', 'official_docs'
 UNION ALL SELECT 'Kubernetes Native', 'Operations', 'Community operators available (not official)', 'expert'
 UNION ALL SELECT 'Backup & Restore', 'Operations', 'mysqldump, mysqlpump, Percona XtraBackup, PITR via binlog', 'official_docs'
 UNION ALL SELECT 'Monitoring & Observability', 'Operations', 'Performance Schema, sys schema, PMM', 'official_docs'
 UNION ALL SELECT 'Pricing Model', 'Cost', 'Open source (GPL); managed service pricing varies', 'official_docs'
 UNION ALL SELECT 'Free Tier', 'Cost', 'Open source free; cloud free tiers vary by provider', 'official_docs'
 UNION ALL SELECT 'TCO at Scale', 'Cost', 'Low at small scale; sharding adds operational cost', 'expert'
 UNION ALL SELECT 'RPO/RTO', 'Reliability', 'RPO depends on replication lag; RTO minutes with failover', 'expert'
 UNION ALL SELECT 'Multi-Region', 'Reliability', 'Async replication across regions; no native multi-region', 'official_docs'
 UNION ALL SELECT 'Automatic Failover', 'Reliability', 'InnoDB Cluster / Group Replication with auto-failover', 'official_docs'
 UNION ALL SELECT 'Data Encryption', 'Reliability', 'TLS in transit, InnoDB tablespace encryption at rest', 'official_docs'
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE p.name = 'MySQL';

-- PostgreSQL feature values
INSERT INTO product_features (product_id, feature_id, value, source)
SELECT p.id, f.id, m.val, m.src FROM products p,
(SELECT 'Horizontal Scaling' AS fname, 'Scalability' AS fcat, 'Limited native - Citus extension for sharding' AS val, 'official_docs' AS src
 UNION ALL SELECT 'Auto-Sharding', 'Scalability', 'Not native - Citus or manual partitioning', 'official_docs'
 UNION ALL SELECT 'Max Cluster Size', 'Scalability', 'Single primary; streaming replication for read replicas', 'official_docs'
 UNION ALL SELECT 'Elastic Scaling', 'Scalability', 'Vertical scaling; read replicas for read workloads', 'official_docs'
 UNION ALL SELECT 'MySQL Compatibility', 'SQL Compatibility', 'Not compatible', 'official_docs'
 UNION ALL SELECT 'PostgreSQL Compatibility', 'SQL Compatibility', 'Native - the reference implementation', 'official_docs'
 UNION ALL SELECT 'Distributed SQL', 'SQL Compatibility', 'Not native (Citus adds distributed queries)', 'official_docs'
 UNION ALL SELECT 'ACID Transactions', 'SQL Compatibility', 'Full ACID with MVCC (single node)', 'official_docs'
 UNION ALL SELECT 'Read Latency (p99)', 'Performance', '< 5ms for point queries (single node)', 'benchmark'
 UNION ALL SELECT 'Write Throughput', 'Performance', '10K-50K TPS (single node, hardware dependent)', 'benchmark'
 UNION ALL SELECT 'HTAP Capability', 'Performance', 'Analytical extensions available (columnar, parallel query)', 'official_docs'
 UNION ALL SELECT 'Query Optimizer', 'Performance', 'Advanced cost-based optimizer with extensive statistics', 'official_docs'
 UNION ALL SELECT 'Vector Search', 'AI/ML', 'pgvector extension - mature vector similarity search', 'official_docs'
 UNION ALL SELECT 'JSON/Document Support', 'AI/ML', 'JSONB with rich operators, indexing, and path queries', 'official_docs'
 UNION ALL SELECT 'Change Data Capture', 'AI/ML', 'Logical replication, Debezium, wal2json', 'official_docs'
 UNION ALL SELECT 'ML Integration', 'AI/ML', 'pgml, MADlib, and Python/R procedural languages', 'official_docs'
 UNION ALL SELECT 'Managed Service', 'Operations', 'RDS PostgreSQL, Azure PostgreSQL, Cloud SQL, Supabase', 'official_docs'
 UNION ALL SELECT 'Kubernetes Native', 'Operations', 'CloudNativePG, Zalando Postgres Operator', 'expert'
 UNION ALL SELECT 'Backup & Restore', 'Operations', 'pg_dump, pg_basebackup, pgBackRest, Barman, PITR', 'official_docs'
 UNION ALL SELECT 'Monitoring & Observability', 'Operations', 'pg_stat_statements, pgBadger, pgwatch2', 'official_docs'
 UNION ALL SELECT 'Pricing Model', 'Cost', 'Open source (PostgreSQL License); managed pricing varies', 'official_docs'
 UNION ALL SELECT 'Free Tier', 'Cost', 'Open source free; Supabase/Neon offer free tiers', 'official_docs'
 UNION ALL SELECT 'TCO at Scale', 'Cost', 'Low at small scale; scaling requires careful architecture', 'expert'
 UNION ALL SELECT 'RPO/RTO', 'Reliability', 'RPO depends on replication; RTO minutes with Patroni', 'expert'
 UNION ALL SELECT 'Multi-Region', 'Reliability', 'Async replication; BDR for multi-master', 'official_docs'
 UNION ALL SELECT 'Automatic Failover', 'Reliability', 'Patroni, repmgr, or pg_auto_failover', 'official_docs'
 UNION ALL SELECT 'Data Encryption', 'Reliability', 'TLS in transit, pgcrypto, TDE in some forks', 'official_docs'
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE p.name = 'PostgreSQL';

-- PLACEHOLDER_EXPERT_ADVICE

-- CockroachDB feature values (partial - key differentiators)
INSERT INTO product_features (product_id, feature_id, value, source)
SELECT p.id, f.id, m.val, m.src FROM products p,
(SELECT 'Horizontal Scaling' AS fname, 'Scalability' AS fcat, 'Native horizontal scaling with automatic rebalancing' AS val, 'official_docs' AS src
 UNION ALL SELECT 'Auto-Sharding', 'Scalability', 'Automatic range-based sharding', 'official_docs'
 UNION ALL SELECT 'Distributed SQL', 'SQL Compatibility', 'Full distributed SQL with serializable isolation', 'official_docs'
 UNION ALL SELECT 'ACID Transactions', 'SQL Compatibility', 'Distributed ACID with serializable isolation', 'official_docs'
 UNION ALL SELECT 'PostgreSQL Compatibility', 'SQL Compatibility', 'PostgreSQL wire protocol compatible', 'official_docs'
 UNION ALL SELECT 'MySQL Compatibility', 'SQL Compatibility', 'Not supported', 'official_docs'
 UNION ALL SELECT 'Multi-Region', 'Reliability', 'Native multi-region with locality-aware queries', 'official_docs'
 UNION ALL SELECT 'Automatic Failover', 'Reliability', 'Automatic via Raft consensus', 'official_docs'
 UNION ALL SELECT 'Managed Service', 'Operations', 'CockroachDB Cloud (Dedicated and Serverless)', 'official_docs'
 UNION ALL SELECT 'Vector Search', 'AI/ML', 'pgvector-compatible vector search support', 'official_docs'
 UNION ALL SELECT 'Read Latency (p99)', 'Performance', '< 10ms local reads; cross-region adds latency', 'benchmark'
 UNION ALL SELECT 'Write Throughput', 'Performance', 'High with horizontal scaling; consensus overhead per write', 'benchmark'
) m
JOIN features f ON f.name = m.fname AND f.category = m.fcat
WHERE p.name = 'CockroachDB';

-- ============================================================
-- Expert Advice
-- ============================================================

-- AI Agent: TiDB vs MySQL
INSERT INTO expert_advice (industry_id, product_a_id, product_b_id, advice_text, author)
SELECT s.id, pa.id, pb.id,
'For AI Agent workloads, TiDB offers a significant advantage with its native vector search capability and HTAP architecture. The TiFlash columnar engine enables real-time analytics on the same data used for transactional AI operations, eliminating the need for a separate analytics pipeline. MySQL lacks native vector search and requires external solutions like Elasticsearch for similarity queries.',
'Database Architecture Team'
FROM industries s, products pa, products pb
WHERE s.name = 'AI' AND pa.name = 'TiDB' AND pb.name = 'MySQL';

INSERT INTO expert_advice (industry_id, product_a_id, product_b_id, advice_text, author)
SELECT s.id, pa.id, pb.id,
'When building RAG pipelines, TiDB''s ability to store both structured data and vector embeddings in a single database simplifies the architecture significantly. With MySQL, teams typically need to maintain a separate vector database (Pinecone, Milvus) alongside MySQL, increasing operational complexity and data synchronization challenges.',
'AI Platform Engineering'
FROM industries s, products pa, products pb
WHERE s.name = 'AI' AND pa.name = 'TiDB' AND pb.name = 'MySQL';

-- AI Agent: TiDB vs PostgreSQL
INSERT INTO expert_advice (industry_id, product_a_id, product_b_id, advice_text, author)
SELECT s.id, pa.id, pb.id,
'PostgreSQL with pgvector is a strong contender for AI workloads. However, TiDB''s distributed architecture provides better horizontal scalability for large-scale embedding storage and retrieval. For teams already using MySQL-compatible stacks, TiDB offers a smoother migration path while adding vector capabilities.',
'AI Platform Engineering'
FROM industries s, products pa, products pb
WHERE s.name = 'AI' AND pa.name = 'TiDB' AND pb.name = 'PostgreSQL';

-- E-Commerce: TiDB vs MySQL
INSERT INTO expert_advice (industry_id, product_a_id, product_b_id, advice_text, author)
SELECT s.id, pa.id, pb.id,
'For e-commerce at scale, TiDB eliminates the painful MySQL sharding journey. Many e-commerce platforms hit MySQL scaling limits during flash sales and peak events. TiDB''s distributed transactions and automatic sharding handle these spikes natively, while maintaining MySQL compatibility for existing application code.',
'E-Commerce Platform Team'
FROM industries s, products pa, products pb
WHERE s.name = 'eCommerce' AND pa.name = 'TiDB' AND pb.name = 'MySQL';

INSERT INTO expert_advice (industry_id, product_a_id, product_b_id, advice_text, author)
SELECT s.id, pa.id, pb.id,
'TiDB''s HTAP capability is a game-changer for e-commerce analytics. Real-time dashboards for inventory, sales, and customer behavior can query the same database serving transactions, without ETL delays or stale data. MySQL requires a separate analytics database and ETL pipeline for similar functionality.',
'Data Analytics Team'
FROM industries s, products pa, products pb
WHERE s.name = 'eCommerce' AND pa.name = 'TiDB' AND pb.name = 'MySQL';

-- Gaming: TiDB vs MySQL
INSERT INTO expert_advice (industry_id, product_a_id, product_b_id, advice_text, author)
SELECT s.id, pa.id, pb.id,
'Gaming backends demand consistent low latency and high throughput for player state management. TiDB provides these at scale without the operational burden of managing MySQL shards. For global games, TiDB''s multi-region deployment with Placement Rules enables data locality for players in different regions.',
'Gaming Backend Architecture'
FROM industries s, products pa, products pb
WHERE s.name = 'Gaming' AND pa.name = 'TiDB' AND pb.name = 'MySQL';

-- Financial Services: TiDB vs MySQL
INSERT INTO expert_advice (industry_id, product_a_id, product_b_id, advice_text, author)
SELECT s.id, pa.id, pb.id,
'Financial services require strong consistency and zero data loss. TiDB''s Raft-based replication provides RPO=0 with synchronous replication across replicas. Combined with distributed ACID transactions, it meets the stringent requirements of financial workloads while scaling horizontally — something MySQL cannot achieve without significant middleware complexity.',
'Financial Systems Architecture'
FROM industries s, products pa, products pb
WHERE s.name = 'Fintech' AND pa.name = 'TiDB' AND pb.name = 'MySQL';

-- Financial Services: TiDB vs PostgreSQL
INSERT INTO expert_advice (industry_id, product_a_id, product_b_id, advice_text, author)
SELECT s.id, pa.id, pb.id,
'PostgreSQL offers excellent single-node consistency and a rich feature set for financial applications. However, when transaction volumes exceed single-node capacity, TiDB''s native distributed architecture avoids the complexity of Citus or custom sharding solutions. For MySQL-based financial systems looking to scale, TiDB is a more natural migration path.',
'Financial Systems Architecture'
FROM industries s, products pa, products pb
WHERE s.name = 'Fintech' AND pa.name = 'TiDB' AND pb.name = 'PostgreSQL';

-- ============================================================
-- Case Studies (TiDB)
-- ============================================================

-- AI
INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'AI-Powered Content Recommendation Platform',
'Zhihu (China''s Quora)',
'Zhihu migrated from MySQL sharding to TiDB to support its AI-driven content recommendation engine. The platform needed to handle real-time feature extraction and vector-based similarity queries across billions of user interactions.',
'3x improvement in recommendation latency; eliminated manual sharding overhead; unified OLTP and OLAP workloads on a single TiDB cluster'
FROM industries i, products p WHERE i.name = 'AI' AND p.name = 'TiDB';

INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Real-Time ML Feature Store',
'PalFish (Online Education)',
'PalFish built a real-time ML feature store on TiDB to power AI-based student-teacher matching. TiDB''s HTAP capability allowed them to run analytical queries for feature engineering alongside transactional workloads without data replication.',
'Reduced feature freshness from hours to seconds; simplified architecture by removing separate analytics database'
FROM industries i, products p WHERE i.name = 'AI' AND p.name = 'TiDB';

-- Gaming
INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Global Game State Management',
'JEJOUE (Mobile Gaming)',
'JEJOUE adopted TiDB to manage player state, inventory, and leaderboard data across global regions. TiDB''s multi-region deployment with Placement Rules ensured low-latency reads for players worldwide.',
'Sub-10ms p99 read latency for player state; zero-downtime scaling during game launch events'
FROM industries i, products p WHERE i.name = 'Gaming' AND p.name = 'TiDB';

INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Real-Time Leaderboard and Matchmaking',
'Cocos (Game Engine Platform)',
'Cocos migrated its backend services from MySQL to TiDB to handle massive concurrent matchmaking and leaderboard queries during peak gaming hours without manual sharding.',
'10x throughput improvement during peak hours; eliminated sharding complexity for game developers'
FROM industries i, products p WHERE i.name = 'Gaming' AND p.name = 'TiDB';

-- eCommerce
INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Flash Sale Transaction Processing',
'Shopee (Southeast Asia eCommerce)',
'Shopee deployed TiDB to handle flash sale events with extreme traffic spikes. TiDB''s distributed ACID transactions ensured inventory consistency while scaling horizontally to absorb 10x normal traffic.',
'Handled 100K+ TPS during flash sales; zero overselling incidents; MySQL-compatible migration with minimal code changes'
FROM industries i, products p WHERE i.name = 'eCommerce' AND p.name = 'TiDB';

INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Omnichannel Inventory and Analytics',
'Xiaomi (Consumer Electronics)',
'Xiaomi uses TiDB for real-time inventory tracking across online and offline channels. TiFlash provides instant sales analytics dashboards without ETL pipelines.',
'Real-time inventory visibility across 10,000+ retail points; 90% reduction in analytics query time via HTAP'
FROM industries i, products p WHERE i.name = 'eCommerce' AND p.name = 'TiDB';

-- Fintech
INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Core Banking Ledger System',
'WeBank (Digital Bank)',
'WeBank replaced its MySQL-based core ledger with TiDB to achieve distributed ACID transactions at scale. The system handles hundreds of millions of accounts with strong consistency and RPO=0.',
'Supports 200M+ accounts; RPO=0 with Raft replication; passed regulatory compliance audits for financial data'
FROM industries i, products p WHERE i.name = 'Fintech' AND p.name = 'TiDB';

INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Real-Time Risk Assessment Platform',
'ZhongAn Insurance (InsurTech)',
'ZhongAn built its real-time risk scoring engine on TiDB, combining transactional policy data with analytical risk models using HTAP capabilities.',
'Risk assessment latency reduced from minutes to sub-second; unified transactional and analytical workloads'
FROM industries i, products p WHERE i.name = 'Fintech' AND p.name = 'TiDB';

-- SaaS
INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Multi-Tenant Data Platform',
'Meituan (Super App Platform)',
'Meituan migrated multiple MySQL clusters to TiDB for its SaaS-like internal platform serving dozens of business units. TiDB''s elastic scaling handles varying tenant workloads without over-provisioning.',
'Consolidated 20+ MySQL clusters into 3 TiDB clusters; 60% reduction in DBA operational overhead'
FROM industries i, products p WHERE i.name = 'SaaS' AND p.name = 'TiDB';

INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Elastic SaaS Backend',
'VIPKid (Online Education SaaS)',
'VIPKid uses TiDB as the backend for its multi-tenant education platform, dynamically scaling compute and storage based on class scheduling patterns.',
'Seamless scaling from 5K to 50K concurrent sessions; zero downtime during scaling events'
FROM industries i, products p WHERE i.name = 'SaaS' AND p.name = 'TiDB';

-- Retail
INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Unified Retail Data Platform',
'Yihaodian (Walmart China Online)',
'Yihaodian adopted TiDB to unify its POS, inventory, and supply chain databases into a single distributed platform, enabling real-time stock visibility across all stores and warehouses.',
'Real-time inventory sync across 400+ warehouses; 5x faster supply chain reporting via TiFlash'
FROM industries i, products p WHERE i.name = 'Retail' AND p.name = 'TiDB';

INSERT INTO case_studies (industry_id, product_id, title, customer, summary, results)
SELECT i.id, p.id,
'Omnichannel Customer Analytics',
'Li-Ning (Sportswear Retail)',
'Li-Ning uses TiDB to power its omnichannel customer analytics platform, combining in-store POS data with online shopping behavior for personalized marketing.',
'360-degree customer view across 7,000+ stores; campaign targeting latency reduced from days to minutes'
FROM industries i, products p WHERE i.name = 'Retail' AND p.name = 'TiDB';



