"""Apply the profile's visual identity to the generated public GitHub data.

The pinned Stats Extended action remains responsible for fetching the metrics.
This step reads its SVG values; it never estimates or changes the numbers.
"""

from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ASSETS = Path(__file__).resolve().parents[1] / 'assets' / 'profile'
PALETTES = {
    'dark': dict(bg='#10172a', end='#16162f', border='#29354e',
                 text='#f1f5ff', muted='#a9b8d1', tile='#19263d',
                 dot='#26334d', violet='#a78bfa', cyan='#22d3ee'),
    'light': dict(bg='#f6f8ff', end='#eef3ff', border='#d6def0',
                  text='#17233c', muted='#52637e', tile='#ffffff',
                  dot='#dbe3f5', violet='#7c3aed', cyan='#0e7490'),
}
LANGUAGE_COLORS = ('#8b5cf6', '#06b6d4', '#3b82f6', '#f97316', '#10b981', '#ec4899')


def source_values(path):
    root = ET.parse(path).getroot()
    if 'Something went wrong' in ''.join(root.itertext()):
        raise ValueError(f'Upstream returned an error card: {path}')
    values = {}
    for key in ('commits', 'stars', 'prs', 'issues', 'contribs'):
        nodes = root.findall(f".//*[@data-testid='{key}']")
        if len(nodes) == 1:
            value = ''.join(nodes[0].itertext()).strip()
            if not re.fullmatch(r'\d[\d,.]*[kKmMbB]?', value):
                raise ValueError(f'Invalid {key} value: {path}')
            values[key] = value
    languages = []
    for node in root.findall(".//*[@data-testid='lang-name']"):
        label = ' '.join(''.join(node.itertext()).split())
        match = re.fullmatch(r'(.+?)\s+(\d+(?:\.\d+)?)%', label)
        if not match:
            raise ValueError(f'Invalid language value: {path}')
        languages.append((match[1], match[2]))
    return values, languages


def shell(theme, title, description, kicker, icon, body):
    p = PALETTES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="320" viewBox="0 0 480 320" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs>
    <linearGradient id="bg" x2="1" y2="1"><stop stop-color="{p['bg']}"/><stop offset="1" stop-color="{p['end']}"/></linearGradient>
    <linearGradient id="accent"><stop stop-color="#8b5cf6"/><stop offset="1" stop-color="#06b6d4"/></linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1" fill="{p['dot']}"/></pattern>
    <clipPath id="card"><rect x="1" y="1" width="478" height="318" rx="22"/></clipPath>
    <clipPath id="bar"><rect x="28" y="116" width="424" height="14" rx="7"/></clipPath>
  </defs>
  <rect x="1" y="1" width="478" height="318" rx="22" fill="url(#bg)" stroke="{p['border']}"/>
  <g clip-path="url(#card)">
    <rect width="480" height="320" fill="url(#dots)"/>
    <circle cx="465" cy="0" r="125" fill="#8b5cf6" opacity=".055"/>
    <circle cx="20" cy="330" r="110" fill="#06b6d4" opacity=".04"/>
    <path d="M29 1h90" stroke="url(#accent)" stroke-width="3"/>
  </g>
  <g font-family="Segoe UI, Arial, sans-serif">
    <text x="28" y="34" fill="{p['violet']}" font-size="10" font-weight="700" letter-spacing="1.8">{kicker}</text>
    <text x="28" y="71" fill="{p['text']}" font-size="28" font-weight="750" letter-spacing="-.8">{escape(title)}</text>
    <rect x="404" y="22" width="48" height="48" rx="15" fill="{p['tile']}" stroke="{p['border']}"/>
    <g transform="translate(416 34)" fill="none" stroke="{p['violet']}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{icon}</g>
    {body}
  </g>
</svg>
'''


def stats_card(theme, values):
    if set(values) != {'commits', 'stars', 'prs', 'issues', 'contribs'}:
        raise ValueError('The source stats card is missing a metric')
    p = PALETTES[theme]
    body = []
    for x, key, label, accent in (
        (28, 'commits', 'Commits · last year', p['violet']),
        (250, 'stars', 'Stars earned', p['cyan']),
    ):
        body.append(f'''<rect x="{x}" y="99" width="202" height="108" rx="16" fill="{p['tile']}" stroke="{p['border']}"/>
    <text x="{x + 18}" y="156" data-testid="{key}" fill="{accent}" font-size="46" font-weight="750" letter-spacing="-1.5">{escape(values[key])}</text>
    <text x="{x + 19}" y="183" fill="{p['muted']}" font-size="12" font-weight="600">{label}</text>''')
    for x, key, label in ((28, 'prs', 'Pull requests'), (178, 'issues', 'Issues'),
                          (316, 'contribs', 'Repos · last year')):
        body.append(f'''<text x="{x}" y="246" data-testid="{key}" fill="{p['text']}" font-size="26" font-weight="700">{escape(values[key])}</text>
    <text x="{x}" y="267" fill="{p['muted']}" font-size="11">{label}</text>''')
    body.append(f'''<path d="M28 285h424" stroke="{p['border']}"/>
    <circle cx="32" cy="302" r="3" fill="{p['cyan']}"/>
    <text x="43" y="305" fill="{p['muted']}" font-size="10">Public GitHub activity</text>
    <text x="452" y="305" text-anchor="end" fill="{p['muted']}" font-size="10">@khayem487</text>''')
    description = (f"Public GitHub statistics: {values['commits']} commits in the last year, "
                   f"{values['stars']} stars earned, {values['prs']} pull requests, "
                   f"{values['issues']} issues, {values['contribs']} repositories contributed to in the last year.")
    return shell(theme, 'Code, in motion.', description, '01 / OPEN SOURCE',
                 '<path d="m8 5-6 7 6 7m8-14 6 7-6 7m-3-16-3 18"/>', ''.join(body))


def languages_card(theme, languages):
    if not 1 <= len(languages) <= 6:
        raise ValueError('Expected one to six languages from the compact source card')
    if not 99 <= sum(float(value) for _, value in languages) <= 101:
        raise ValueError('Language percentages do not sum to approximately 100')
    p = PALETTES[theme]
    body = [f'<text x="28" y="95" fill="{p["muted"]}" font-size="12">Most used languages in public repositories</text>']
    cursor = 28.0
    for index, (name, value) in enumerate(languages):
        color = LANGUAGE_COLORS[index]
        width = 424 * float(value) / 100
        body.append(f'<rect x="{cursor:.3f}" y="116" width="{width:.3f}" height="14" fill="{color}" clip-path="url(#bar)"/>')
        cursor += width
        x, y = 28 + (index // 3) * 222, 171 + (index % 3) * 43
        body.append(f'''<circle cx="{x + 4}" cy="{y - 5}" r="4" fill="{color}"/>
    <text data-testid="lang-name" x="{x + 17}" y="{y}" fill="{p['text']}" font-size="13" font-weight="600"><tspan>{escape(name)} </tspan><tspan x="{x + 202}" text-anchor="end" fill="{p['muted']}" font-size="12" font-weight="400">{value}%</tspan></text>''')
    body.append(f'''<path d="M28 285h424" stroke="{p['border']}"/>
    <text x="28" y="305" fill="{p['muted']}" font-size="10">By code size · selected languages, not proficiency</text>''')
    description = 'Public repository language distribution: ' + ', '.join(f'{name} {value}%' for name, value in languages)
    return shell(theme, 'Behind the builds.', description, '02 / CODE PALETTE',
                 '<path d="M3 20V10m6 10V4m6 16v-7m6 7V7"/>', ''.join(body))


def main():
    output = {}
    for theme in PALETTES:
        stats_path = ASSETS / f'github-stats-{theme}.svg'
        languages_path = ASSETS / f'github-languages-{theme}.svg'
        values, _ = source_values(stats_path)
        _, languages = source_values(languages_path)
        output[stats_path] = stats_card(theme, values)
        output[languages_path] = languages_card(theme, languages)
    # Parse every result before touching any of the last successful cards.
    for text in output.values():
        ET.fromstring(text)
    for path, text in output.items():
        path.write_text(text, encoding='utf-8')
        print(f'Styled {path.name}')


if __name__ == '__main__':
    main()
