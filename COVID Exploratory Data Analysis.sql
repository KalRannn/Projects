
--DEATH PERCENTAGE BASED ON TOTAL CASES AND TOTAL DEATHS IN COUNTRY 
SELECT Location, date, total_cases, total_deaths, ((total_deaths*1.0/total_cases)*100) as [Death%]
FROM [PortfolioProject].[dbo].['Covid Deaths$']
WHERE continent is NOT NULL
ORDER BY 1,2 

--WHAT PERTANGE OF THE POPULATION HAS GOTTEN COVID
SELECT Location, date, population,total_cases, ((total_cases*1.0/population)*100) as [CovidTested]
FROM [PortfolioProject].[dbo].['Covid Deaths$']
WHERE continent is NOT NULL
AND Location LIKE '%Canada%'
ORDER BY 1,2 

--WHAT COUNTRIES HAVE THE HIGHEST INFECTION RATE
SELECT Location, population,MAX(total_cases)as MaxCases, MAX((total_cases*1.0/population))*100 as [%Infected]
FROM [PortfolioProject].[dbo].['Covid Deaths$']
WHERE continent is NOT NULL
GROUP BY Location, population
ORDER BY 4 DESC

--WHAT COUNTRIES HAVE THE HIGHEST DEATH RATE
SELECT Location, population,MAX(total_deaths)as MaxDeaths, MAX((total_deaths*1.0/population))*100 as [%Deaths]
FROM [PortfolioProject].[dbo].['Covid Deaths$']
WHERE continent is NOT NULL
GROUP BY Location, population
ORDER BY 4 DESC

--WHAT CONTINENT HAVE THE HIGHEST DEATH RATE
SELECT continent, MAX(total_deaths)as MaxDeaths, MAX((total_deaths*1.0/population))*100 as [%Deaths]
FROM [PortfolioProject].[dbo].['Covid Deaths$']
WHERE continent is NOT NULL
GROUP BY continent
ORDER BY 2 DESC

--GLOBAL NUMBERS
SELECT date, SUM(new_cases)as Cases,SUM(cast(new_deaths as int))as Deaths, (SUM(new_deaths)/NULLIF(SUM(new_cases), 0)) as [DEATHS%]
FROM [PortfolioProject].[dbo].['Covid Deaths$']
WHERE continent is NOT NULL
GROUP BY date
ORDER BY 2

--LOOK AT TOTAL POPULATION VS VACCINATIONS
WITH PopvsVac (Continent, Location, Date, Population,New_Vaccinations,RollingPeopleVaccinated)
AS
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(cast(vac.new_vaccinations as BIGINT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100


FROM [dbo].['Covid Deaths$'] dea
JOIN [dbo].[CovidVaccinations$] vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent is NOT NULL
--ORDER BY 2,3
)
SELECT *, (RollingPeopleVaccinated/Population)*100
FROM PopvsVac

--TEMP TABLE
DROP TABLE IF EXISTS #PercentPopVacc
CREATE TABLE #PercentPopVacc(
Continent NVARCHAR(255),
Location NVARCHAR(255),
Date datetime,
Population NUMERIC,
New_Vaccinations NUMERIC,
RollingPeopleVaccinated NUMERIC
)
INSERT INTO #PercentPopVacc
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(cast(vac.new_vaccinations as BIGINT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100


FROM [dbo].['Covid Deaths$'] dea
JOIN [dbo].[CovidVaccinations$] vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent is NOT NULL
--ORDER BY 2,3

SELECT *, (RollingPeopleVaccinated/Population)*100
FROM #PercentPopVacc

CREATE VIEW PercentPopVacc as
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(cast(vac.new_vaccinations as BIGINT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100


FROM [dbo].['Covid Deaths$'] dea
JOIN [dbo].[CovidVaccinations$] vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent is NOT NULL
--ORDER BY 2,3

SELECT *
FROM PercentPopVacc
