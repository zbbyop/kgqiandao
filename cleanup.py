import os
import requests

# 获取环境变量
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY', 'zbbyop/opwpy')  # 替换为你的仓库路径
REPO_TOKEN = os.getenv('REPO_TOKEN')

# 获取 Workflow 名称（不是文件名）
CURRENT_WORKFLOW_NAME = os.getenv('GITHUB_WORKFLOW', '').strip()

# 如果没有获取到 workflow 名称，则抛出异常
if not CURRENT_WORKFLOW_NAME:
    raise ValueError("Unable to determine the current workflow name from the environment.")

# 获取 workflow 文件的 ID
workflows_api_url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/actions/workflows'
response = requests.get(workflows_api_url, headers={'Authorization': f'token {REPO_TOKEN}'})
response.raise_for_status()
workflows = response.json()['workflows']

workflow_id = next((w['id'] for w in workflows if w['name'].strip().lower() == CURRENT_WORKFLOW_NAME.lower()), None)

if workflow_id is None:
    raise ValueError(f'Workflow "{CURRENT_WORKFLOW_NAME}" not found in repository {GITHUB_REPOSITORY}')

# 获取特定 workflow 的运行记录
workflow_runs_api_url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/actions/workflows/{workflow_id}/runs'
response = requests.get(workflow_runs_api_url, headers={'Authorization': f'token {REPO_TOKEN}'})
response.raise_for_status()
workflow_runs = response.json()['workflow_runs']

# 删除旧的 workflow 运行记录
for run in workflow_runs:
    run_id = run['id']
    run_url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/actions/runs/{run_id}'
    response = requests.delete(run_url, headers={'Authorization': f'token {REPO_TOKEN}'})
    if response.status_code == 204:
        print(f'Successfully deleted run {run_id} for workflow {CURRENT_WORKFLOW_NAME}')
    else:
        print(f'Failed to delete run {run_id} for workflow {CURRENT_WORKFLOW_NAME}: {response.status_code} - {response.text}')
