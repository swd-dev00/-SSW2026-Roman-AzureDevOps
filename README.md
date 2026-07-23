# SSW2026 Roman Dark Lens + SED Fitting

Azure DevOps repository for the advanced combined Sagan Summer Workshop project.

## Contents

- Official SED-fitting structure merged with advanced dark-lens analysis
- Azure DevOps YAML pipeline
- SPISEA environment validation
- Persistent isochrone generation
- Workshop data validation
- Automated notebook execution
- Pipeline artifact publishing

## Required infrastructure

- Azure DevOps self-hosted Linux agent pool named `SPISEA-Linux`
- Azure VM with Docker
- Persistent project path: `/mnt/ssw2026/project`
- Docker image: `amigahub/spisea:v1`

## Required workshop files

Upload once to `/mnt/ssw2026/project/data/`:

- `events_table.parquet`
- `stars_table.parquet`
- `sim_pops_table.parquet`

## Pipeline

Import `azure-pipelines.yml` as an existing YAML pipeline.

Runtime parameters:

- `generateIsochrones`
- `executeNotebook`

The generated isochrones remain on the persistent Azure disk. The executed notebook and compact outputs are published as the `roman-spisea-results` pipeline artifact.

## Notebook patch

Azure-compatible notebook path conversion applied: **yes**.
