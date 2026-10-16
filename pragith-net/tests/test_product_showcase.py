from html.parser import HTMLParser

from fastapi.testclient import TestClient

from app.content.site import PROJECTS
from app.main import app, PACKAGE_VERSION

client = TestClient(app, base_url='http://localhost')


class Elements(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def test_homepage_curates_three_products_after_professional_work():
    html = client.get('/').text
    elements = Elements(html).elements
    assert [attrs['data-testid'] for tag, attrs in elements if tag == 'article' and 'data-testid' in attrs] == [
        'project-quantum-lab', 'project-golf-swing-analyzer', 'project-jasoos',
    ]
    assert html.index('Enterprise AI assistant') < html.index('project-quantum-lab')
    assert 'Velvet IPTV Player' not in html
    assert 'Fairway' not in html and 'golf.lab.pragith.net' not in html
    assert 'lesson player, interactive models' in html
    assert 'camera pipeline, pose tracking' in html


def test_full_catalogue_groups_projects_without_losing_existing_entries():
    html = client.get('/projects').text
    assert [p['group'] for p in PROJECTS] == ['products'] * 5 + ['games'] * 2 + ['experiments', 'tools']
    elements = Elements(html).elements
    assert [attrs['aria-labelledby'] for tag, attrs in elements if tag == 'section' and 'aria-labelledby' in attrs] == [
        'products-heading', 'games-heading', 'experiments-heading', 'tools-heading',
    ]
    ids = [attrs['data-testid'] for tag, attrs in elements if tag == 'article' and 'data-testid' in attrs]
    assert len(ids) == len(set(ids)) == 9
    assert ids == [f'project-{p["slug"]}' for p in PROJECTS]
    assert '<pre class="artifact">' not in html
    for title in ['Velvet IPTV Player', 'CallRenard', 'Caffeinate-d', 'Vriksh Cloud', 'Rajadharma', 'Bar None']:
        assert title in html
    assert 'Hosted sessions are in early access' in html
    assert 'installable runtime is planned' in html
    assert 'packaged download is not available' in html
    assert 'source version' not in html.lower().split('project-caffeinate-d')[0]
    assert 'href="https://vriksh.ca/apps"' in html
    assert 'Card Stacks' in html and 'TriviaX Club' in html


def test_product_destinations_and_screenshot_candidates_resolve():
    html = client.get('/projects').text
    elements = Elements(html).elements
    links = [attrs['href'] for tag, attrs in elements if tag == 'a']
    for url in ['https://learnquantum.science/', 'https://aperture.golf/', 'https://analyze.aperture.golf/', 'https://jasoos.me/', 'https://vriksh.ca/apps/callrenard', 'https://play.rajadharma.in/', 'https://barnone.lab.pragith.net/']:
        assert url in links
    assert 'https://vriksh.ca/ventures/callrenard' not in links
    for tag, attrs in elements:
        if tag != 'img':
            continue
        assert attrs['alt'] and int(attrs['width']) > 0 and int(attrs['height']) > 0
        for path in [attrs['src'], *(candidate.strip().split()[0] for candidate in attrs['srcset'].split(','))]:
            assert client.get(path).status_code == 200, path
    assert 'Big Buck Bunny' in html and 'https://creativecommons.org/licenses/by/3.0/' in html
    assert client.get('/projects/caffeinate-d').status_code == 200


def test_teaching_exposes_live_course_and_about_derives_manifest_version():
    html = client.get('/teaching').text
    assert 'Learn with Quantum Lab' in html
    assert 'href="https://learnquantum.science/"' in html
    assert 'simulations and save your progress' in html
    assert 'Discuss a course or workshop' in html
    assert f'Website version {PACKAGE_VERSION}' in client.get('/about').text
    assert PACKAGE_VERSION == '1.2.2'


def test_studio_ownership_is_prominent_and_simulator_is_linked_with_context():
    home = client.get('/').text
    assert home.index('studio I founded and run') < home.index('Professional experience')
    assert 'through <a href="https://vriksh.ca/">Vriksh</a>, the Canadian software studio I founded and run.' in home
    for path in ['/projects', '/about']:
        html = client.get(path).text
        assert 'I founded and run <a href="https://vriksh.ca/">Vriksh</a>' in html
        assert 'My studio: Vriksh' in html
    for path in ['/', '/projects']:
        html = client.get(path).text
        assert 'href="https://sim.aperture.golf/"' in html
        assert 'aim, choose a club and set shot power' in html
        assert 'href="https://analyze.aperture.golf/"' in html
        assert 'href="https://aperture.golf/"' in html
