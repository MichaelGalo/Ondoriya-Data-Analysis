-- KPI: Total Population = count of all individuals from people
CREATE TABLE IF NOT EXISTS CLEANED.TOTAL_POPULATION AS
SELECT COUNT(*) AS TOTAL_POPULATION
FROM STAGED.PEOPLE;

-- KPI: Dominant Faction = name of the faction with the highest percentage
CREATE TABLE IF NOT EXISTS CLEANED.DOMINANT_FACTION AS
SELECT
    Faction, MAX(Percent) AS max_percent
FROM STAGED.FACTION_DISTRIBUTION
GROUP BY Faction
ORDER BY max_percent DESC
LIMIT 1 OFFSET 1; -- offset to avoid the total

-- Visualization: Population Density by Region
CREATE TABLE IF NOT EXISTS CLEANED.POPULATION_DENSITY AS
SELECT
    r.Colloquial_Name,
    COUNT(p.id) AS population
FROM STAGED.PEOPLE p
JOIN STAGED.HOUSEHOLDS h ON p.household_id = h.id
JOIN STAGED.REGIONS r ON h.region_id = r.id
GROUP BY r.Colloquial_Name
ORDER BY population DESC;

-- Visualization: Distribution
    -- use faction_distribution
CREATE TABLE IF NOT EXISTS CLEANED.FACTION_DISTRIBUTION_CLEANED AS
SELECT
    id,
    Faction,
    Regions,
    Percent
FROM STAGED.FACTION_DISTRIBUTION
ORDER BY Percent DESC;

-- Visualization: Top 5 Most Populous Regions
    -- use regions and people
CREATE TABLE IF NOT EXISTS CLEANED.TOP_5_POPULOUS_REGIONS AS
SELECT
    r.Colloquial_Name,
    COUNT(p.id) AS population
FROM STAGED.REGIONS r
JOIN STAGED.PEOPLE p ON r.id = p.current_region_id
GROUP BY r.Colloquial_Name
ORDER BY population DESC
LIMIT 5;
