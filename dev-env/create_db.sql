
CREATE DATABASE IF NOT EXISTS datawake_prefetch;
USE datawake_prefetch;

CREATE TABLE IF NOT EXISTS datawake_org (
  email VARCHAR(300),
  org VARCHAR(300)
);


CREATE TABLE IF NOT EXISTS datawake_data (
  id INT NOT NULL AUTO_INCREMENT,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  url TEXT,
  userId TEXT,
  userName TEXT,
  trail VARCHAR(100),
  org VARCHAR(300),
  domain VARCHAR(300),
  PRIMARY KEY(id),
  INDEX(url(30))
);


CREATE TABLE IF NOT EXISTS datawake_trails (
  name VARCHAR(100) NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by TEXT,
  description TEXT,
  org VARCHAR(300),
  domain VARCHAR(300),
  PRIMARY KEY(name,org,domain)
);


CREATE TABLE IF NOT EXISTS general_extractor_web_index (
  url varchar(1024),
  entity_type varchar(100),
  entity_value varchar(1024),
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  index(url(300))
);


CREATE TABLE IF NOT EXISTS invalid_extracted_entity (
  entity_value varchar (1024),
  entity_type varchar (100),
  domain varchar (300),
  org VARCHAR(300),
  userName TEXT,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  index(org(300),domain(300), entity_type(100), entity_value(100))
);

CREATE TABLE IF NOT EXISTS trail_based_entities (
  org VARCHAR(300),
  domain varchar(300),
  trail varchar(100) NOT NULL,
  entity varchar(1024),
  google_result_count varchar(100),
  index(org(300), domain(300), trail(100))
);

CREATE TABLE IF NOT EXISTS irrelevant_trail_based_entities (
  org VARCHAR(300),
  domain varchar(300),
  trail varchar(100) NOT NULL,
  entity varchar(1024),
  google_result_count varchar(100),
  index(org(300), domain(300), trail(100))
);

CREATE TABLE IF NOT EXISTS trail_term_rank (
  org VARCHAR(300),
  domain varchar(300),
  trail varchar(100),
  url varchar(2048),
  title varchar(1024),
  rank DOUBLE,
  pageRank INT,
  removed INT DEFAULT 0,
  index(org(300), domain(300), trail(100), url(255))
);

CREATE TABLE IF NOT EXISTS entities_on_url (
  org VARCHAR(300),
  domain varchar(300),
  trail varchar(100),
  url varchar(2024),
  entity varchar(1024),
  relevant INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS trail_entities_contents(
  url varchar(2048),
  html MEDIUMBLOB,
  index(url(255))
);
