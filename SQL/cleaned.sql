-- SQL scripts to feed the dashboard

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


-- Visualization: Top 5 Most Populous Regions
    -- use regions and people


