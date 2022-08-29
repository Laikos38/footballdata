# footballdata

Simple REST API with Django REST Framework and Celery integration for technical interview.

## Set Football-data.org API Key
Register on [Football-data.org](https://www.football-data.org/client/register) and get a free API Key.

Then create an `.env` file in the base directory of the repository and declare the next envvar:
```
FOOTBALL_DATA_ORG_API_KEY=<your-football-data-org-api-key>
```

## Execute
### Docker Compose

#### Local development configuration

```bash
docker-compose -f docker-compose.dev.yaml up --build
```

> The app will run in **http://localhost:7171**

----------------

## Endpoints

### 1. Import league/competition
`http://localhost:7171/api/import-league/<str:league_code>/`

Import league data from Football-data.org (competition, teams, players, coaches).

Params:
- **sync**: bool - Default `false` - Execute the task synchronously.

Leagues/competitions avalaible in free plan of Football-data.org for testing:
`BSA PL ELC CL EC FL1 SA DED PPL CLI PD WC`

### 2. League/competition players
`http://localhost:7171/api/competitions/<str:league_code>/players/`

Imported players participating in the given league/competition.

Params:
- **team_name**: str

### 3. Teams
`http://localhost:7171/api/teams/`

Imported teams.

Params:
- **name**: str
- **include_players**: bool - default `false`

### 4. Players or coaches of a team
`http://localhost:7171/api/teams/players-or-coaches/`

Imported players or coaches of a given team name.

You need to provide a *name* param to get the results.

Params:
- **name**: str

----------------

## Brief explanation of project

[Breve explicación del proyecto.](./docs/project_spanish.md)