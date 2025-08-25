CREATE TABLE IF NOT EXISTS STAGED.FACTION_DISTRIBUTION AS
SELECT
    _record_id AS id,
    Faction,
    Regions,
    Percent
FROM RAW.FACTION_DISTRIBUTION;

CREATE TABLE IF NOT EXISTS STAGED.HOUSEHOLDS AS
SELECT
    household_id AS id,
    region_id,
    household_type
FROM RAW.HOUSEHOLDS;

CREATE TABLE IF NOT EXISTS STAGED.LANGUAGE_BUILDING_BLOCKS AS
SELECT
    Language_ID AS id,
    Language_Name,
    Branch_From,
    Phonology_Notes,
    Morphology_Patterns,
    Example_Roots
FROM RAW.LANGUAGE_BUILDING_BLOCKS;

CREATE TABLE IF NOT EXISTS STAGED.LANGUAGE_ROOTS AS
SELECT
    _record_id AS id,
    Root,
    Meaning,
    Notes
FROM RAW.LANGUAGE_ROOTS;

CREATE TABLE IF NOT EXISTS STAGED.MOONS AS
SELECT
    Moon_ID AS id,
    Moon_Name,
    Settlement_Formal,
    Colloquial,
    Staff_Size,
    Specialty,
    Language_Origin
FROM RAW.MOONS;

CREATE TABLE IF NOT EXISTS STAGED.PEOPLE AS
SELECT
    person_id as id,
    first_name,
    family_name,
    age,
    language,
    current_region_id,
    household_id
FROM RAW.PEOPLE;

CREATE TABLE IF NOT EXISTS STAGED.PLANETS AS
SELECT
    World_ID,
    World_Name,
    Star_System,
    Planet_Type,
    Gravity_g,
    Day_Length_hours,
    Year_Length_days,
    Axial_Tilt_deg,
    Calendar_Name
FROM RAW.PLANETS;

CREATE TABLE IF NOT EXISTS STAGED.REGION_BIOME AS
SELECT
    _record_id as id,
    Full_Name,
    Biome,
    Region_ID
FROM RAW.REGION_BIOME;

CREATE TABLE IF NOT EXISTS STAGED.REGIONS AS
SELECT
    Region_Id as id,
    Ancient_Name,
    Current_Faction,
    Era_Tag,
    Full_Name,
    Colloquial_Name,
    Founding_Era,
    Density_Tier,
    Capital,
    Primary_Industry,
    Founding_Story,
    Vote_History_Last3,
    Key_Pressure_Points,
    Unbound_Presence
FROM RAW.REGIONS;
