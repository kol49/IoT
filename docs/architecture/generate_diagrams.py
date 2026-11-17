"""Generate editable C4 SVG images using Python's standard library."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
NAVY, BLUE, LIGHT, INK = '#16365d', '#2468ac', '#eaf2fa', '#172b43'

def text(x, y, lines, size=21, color=INK, weight='normal', anchor='middle'):
    return ''.join(f'<text x="{x}" y="{y+i*(size+9)}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(line)}</text>' for i, line in enumerate(lines))

def box(x,y,w,h,title,kind,body,fill=BLUE):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}"/>'
            + text(x+w/2,y+39,[title],26,'white','bold')
            + text(x+w/2,y+72,[kind],18,'#e2efff')
            + text(x+w/2,y+112,body,20,'white'))

def arrow(points, x, y, lines):
    return f'<polyline points="{points}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#arrow)"/>' + text(x,y,lines,19)

def frame(title,subtitle,content,legend):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100">'
            '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#172b43"/></marker></defs>'
            '<rect width="1600" height="1100" fill="#ffffff"/>'
            '<g font-family="Arial, Helvetica, sans-serif">'
            + text(65,65,[title],34,INK,'bold','start')
            + text(65,104,[subtitle],20,'#52677d','normal','start')
            + content
            + '<line x1="65" y1="985" x2="1535" y2="985" stroke="#cad7e4"/>'
            + text(65,1022,[legend],18,INK,'normal','start')
            + text(65,1060,['DesignSpace | Proposed MVP architecture | Task #2 | Arrows show the direction of use or data submission.'],18,'#52677d','normal','start')
            + '</g></svg>')

context = box(560,175,480,175,'Designer','[Person]', ['Owns one monitored workspace;', 'sets preferences for creative activities.'],NAVY)
context += arrow('800,350 800,520',460,402,['Pairs a sensor; selects profiles;', 'views conditions, history and alerts'])
context += box(460,530,680,230,'DesignSpace','[Software System]', ['Monitors desk lighting, temperature and humidity.', 'Compares measurements with personal preferences', 'and reports sustained deviations.', 'Includes device firmware and the dashboard service.'])
context += text(800,838,['Scope: one designer, one workspace, one sensor device.', 'No external software service is required by the proposed MVP.', 'Physical sensors are hardware inputs, not separate software systems.'],21)
(ROOT/'system-context.svg').write_text(frame('DesignSpace | C4 Level 1 — System Context','Scope: DesignSpace as a whole • Audience: designers, stakeholders and project reviewers',context,'Key: dark blue = person; blue = software system in scope; solid arrow = labeled relationship.'))

container = '<rect x="65" y="385" width="1470" height="560" rx="12" fill="#f7faff" stroke="#607d9a" stroke-width="2" stroke-dasharray="10 7"/>'
container += text(90,420,['DesignSpace [Software System boundary]'],21,INK,'bold','start')
container += box(80,165,370,160,'Designer','[Person]',['Sets preferences and reviews', 'conditions for creative work.'],NAVY)
container += box(715,155,500,190,'Web Dashboard','[Container: TypeScript / React]', ['Runs in the designer\'s browser.', 'Shows readings, profiles, history,', 'connectivity and in-app alerts.'])
container += arrow('450,245 715,245',580,202,['Uses dashboard', '[Browser UI]'])
# Browser application belongs inside same system via an explicit joined boundary.
container = container.replace('<rect x="65" y="385" width="1470" height="560" rx="12" fill="#f7faff" stroke="#607d9a" stroke-width="2" stroke-dasharray="10 7"/>', '<path d="M65 385 H665 V130 H1535 V945 H65 Z" fill="#f7faff" stroke="#607d9a" stroke-width="2" stroke-dasharray="10 7"/>')
container += box(105,505,440,245,'Sensor Firmware','[Container: C++ / ESP32]', ['Reads light, temperature and humidity', 'from attached sensors via I2C.', 'Timestamps and submits readings', 'every 30 seconds using a device', 'credential; retries transient failures.'])
container += box(715,495,500,255,'Backend API','[Container: Python / FastAPI]', ['Authenticates users and paired devices.', 'Validates readings; manages profiles.', 'Evaluates sustained deviations;', 'serves history and in-app alerts.', 'Computes freshness / offline status.'])
container += arrow('545,620 715,620',630,535,['Submits readings', '[HTTPS / JSON;', 'device credential]'])
container += arrow('965,345 965,495',1175,384,['Pairs devices, updates profiles;', 'polls readings, status and alerts', '[HTTPS / JSON; user session]'])
container += box(715,815,500,100,'Workspace Database','[Container: PostgreSQL]',[])
container += arrow('965,750 965,815',1255,775,['Reads / writes workspace data', '[SQL / TLS]'])
container += text(350,813,['Database stores users, device ownership,', 'profiles, readings and alert state.', '30-day reading retention; 24-hour UI history.'],18)
(ROOT/'container.svg').write_text(frame('DesignSpace | C4 Level 2 — Containers','Scope: applications and data store inside DesignSpace • Technologies are proposed choices',container,'Key: dark blue = person; blue = container; dashed outline = system boundary; arrows = labeled interactions.'))
print('Generated system-context.svg and container.svg')
