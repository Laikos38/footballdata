# footballdata

Simple REST API with Django REST Framework and Celery integration for technical interview.

## Set Football-data.org API Key

## Execute
### Docker Compose
```bash
docker-compose -f docker-compose.dev.yaml up --build
```

> The app will run in **http://localhost:7171**

----------------

## Endpoints

### 1. Import league/competition
`/api/import-league/<str:league_code>/`

Import league data from Football-data.org (competition, teams, players, coaches).

Leagues/competitions avalaible in free plan of Football-data.org for testing:
`BSA PL ELC CL EC FL1 SA DED PPL CLI PD WC`

### 2. League/competition players
`/api/competitions/<str:league_code>/players/`

Imported players participating in the given league/competition.

Params:
- **team_name**: str

### 3. Teams
`/api/teams/`

Imported teams.

Params:
- **name**: str
- **include_players**: bool - default `false`

### 4. Players or coaches of a team
`/api/teams/players-or-coaches/`

Imported players or coaches of a given team name.

Params:
- **name**: str

----------------

## Brief explanation of project

[Brief explanation of project.](./DOCS.md) (spanish)