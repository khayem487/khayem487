"""Refresh the owned public-repository inventory without probing demo servers."""

from pathlib import Path
import json
import os
import re
from urllib.request import Request, urlopen


OWNER = 'khayem487'
SOURCE = f'https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100'
INVENTORY = Path(__file__).resolve().parents[1] / 'assets' / 'profile' / 'highlights.json'


def fetch_public_repos():
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'khayem-profile-cards'}
    if token := os.environ.get('GH_TOKEN'):
        headers['Authorization'] = f'Bearer {token}'
    names = []
    for page in range(1, 11):
        request = Request(f'{SOURCE}&page={page}', headers=headers)
        with urlopen(request, timeout=20) as response:
            if response.status != 200:
                raise ValueError('GitHub did not return a successful repository list')
            repositories = json.load(response)
        if not isinstance(repositories, list):
            raise ValueError('GitHub returned an invalid repository list')
        for repository in repositories:
            if not isinstance(repository, dict):
                raise ValueError('GitHub returned an invalid repository entry')
            if (repository.get('private') is False
                    and repository.get('fork') is False
                    and repository.get('owner', {}).get('login', '').lower() == OWNER):
                name = repository.get('name', '')
                if not re.fullmatch(r'[A-Za-z0-9._-]+', name):
                    raise ValueError('GitHub returned an invalid repository name')
                names.append(name)
        if len(repositories) < 100:
            break
    else:
        raise ValueError('Repository pagination exceeded its safety limit')
    if not names or len(names) != len(set(names)):
        raise ValueError('Expected a nonempty unique inventory; keeping the previous version')
    return sorted(names, key=str.casefold)


def main():
    names = fetch_public_repos()
    data = json.loads(INVENTORY.read_text(encoding='utf-8'))
    data['public_repos'] = {
        'owner': OWNER, 'source': SOURCE, 'exclude_forks': True, 'names': names,
    }
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if content != INVENTORY.read_text(encoding='utf-8'):
        temporary = INVENTORY.with_suffix('.json.tmp')
        temporary.write_text(content, encoding='utf-8')
        temporary.replace(INVENTORY)
    print(f'Reviewed {len(names)} owned public non-fork repositories.')


if __name__ == '__main__':
    main()
