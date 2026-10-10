"""Fill the copied portfolio with fictional photographer details."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent / 'public'
replacements = {
    'Juliette Carlson': 'Aarav Mehta', 'JULI CARLSON': 'AARAV MEHTA',
    'Juli Carlson': 'Aarav Mehta', 'Juli C.': 'Aarav Mehta', 'Juli ': 'Aarav ',
    'julicarlson': 'aaravmehta.photo', 'avalahills': 'aaravmehta.photo',
    'avala_weddings': 'aaravmehta.photo',
    'Avala_weddings@boldthemes.com': 'hello@aaravmehta.example',
    'Avala@boldthemes.com': 'hello@aaravmehta.example',
    '415 Avala Hills Address San Francisco, CA (800) 477-1477': 'Hauz Khas, New Delhi, India<br>+91 00000 00000<br>hello@aaravmehta.example',
    'Avala Hills, 1234 Westside Road, CA': 'Studio 12, Hauz Khas, New Delhi, India',
    '+1 800 100 900': '+91 00000 00000', '(800) 477-1477': '+91 00000 00000',
    'San Francisco, California': 'New Delhi, India', 'San Francisco': 'New Delhi',
    'AVALA - HILLS': 'AARAV MEHTA', 'Copyright 2021 Avala Theme': 'Copyright 2026 Aarav Mehta Photography',
    'Anna &amp; Paul': 'Ananya &amp; Kabir', 'Mary &amp; John': 'Meera &amp; Arjun',
    'Jane &amp; Peter': 'Riya &amp; Dev', 'Anna & Paul': 'Ananya & Kabir',
    'Mary & John': 'Meera & Arjun', 'Jane & Peter': 'Riya & Dev',
    'Coastal Elopement': 'Intimate Wedding in Goa', 'Vineyard Wedding': 'Royal Wedding in Jaipur',
    'Rustic Wedding': 'Garden Wedding in Delhi', 'Destination Wedding': 'Destination Wedding',
    'MINI SESSION': 'PORTRAIT SESSION', 'PER HOUR': 'PRE-WEDDING', 'DAY SESSION': 'WEDDING DAY',
    '40 Minutes Session': '60 Minute Session', '20 Edited Images': '25 Edited Images',
    'Headshots and group portraits': 'Personal and family portraits',
    'THE RISING STAR OF PHOTOGRAPHY BY RE:PHOTO MAGAZINE': 'WEDDINGS, REAL EMOTIONS & TIMELESS STORIES',
    'AWARDS AND REVIEWS': 'THE HEART BEHIND EVERY FRAME',
    'My name is Aarav Mehta and I&#8217;m a wedding, lifestyle and portrait photographer, located in New Delhi, India.': 'I am Aarav Mehta, a wedding and portrait photographer based in New Delhi. For over 8 years, I have captured celebrations across Delhi, Jaipur, Udaipur and Goa.',
    'Over the years I developed my own style and I’m drawn to light and airy. I love natural light and outdoors and if you do too, let’s capture your most important moments together.': 'My approach blends candid storytelling, natural light and thoughtful portraits. From the quiet moments before your ceremony to a dance floor full of laughter, I capture the memories that feel most like you.',
    'Located 5 minutes from the entrance to Lorem ipsum and Dolor Sit Amet Parks, and about 15 minutes from the Westside airport.': 'Our sample studio is based in Hauz Khas, New Delhi. Sessions and consultations are by appointment. Available for weddings and destination shoots across India.',
    'WESTSIDE AIRPORT': 'DELHI & BEYOND', 'THE BEST MUSEUMS': 'YOUR FAVOURITE LOCATIONS',
    'COMFORTABLE BEDS': 'A RELAXED EXPERIENCE',
}
logo = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="135" viewBox="0 0 400 135"><text x="200" y="64" text-anchor="middle" fill="#74776d" font-family="Georgia,serif" font-size="42" font-style="italic">Aarav Mehta</text><text x="200" y="99" text-anchor="middle" fill="#74776d" font-family="Georgia,serif" font-size="13" letter-spacing="7">PHOTOGRAPHY</text></svg>'''
(root / 'portfolio-logo.svg').write_text(logo, encoding='utf-8')
count = 0
for file in root.rglob('*.html'):
    text = file.read_text(encoding='utf-8')
    # Replace longer email strings before social handles.
    for before, after in sorted(replacements.items(), key=lambda pair: -len(pair[0])):
        text = text.replace(before, after)
    text = re.sub(r'(<title>.*?)(?:Autumn)(.*?</title>)', r'\1Aarav Mehta Photography\2', text, flags=re.S)
    text = text.replace('alt="Autumn"', 'alt="Aarav Mehta Photography"')
    text = re.sub(r'(<img\b[^>]*\bsrc=")[^"]*(?:/logo[^/"?]*\.(?:png|avif|jpg)|/footer_logo\.png)(")', r'\1/portfolio-logo.svg\2', text)
    text = re.sub(r'(<span class="bt_bb_price_list_currency">)\$(</span>)', r'\1₹\2', text)
    for before, after in [('175','4,999'),('350','24,999'),('1950','74,999')]:
        text = text.replace('class="bt_bb_price_list_amount">'+before+'<', 'class="bt_bb_price_list_amount">'+after+'<')
    text = text.replace('AWARDS AND REVIEWS', 'THE HEART BEHIND EVERY FRAME')
    text = text.replace('facebook.com/boldthemes/', 'facebook.com/')
    text = text.replace('instagram.com/bold_themes/?hl=en', 'instagram.com/')
    text = text.replace('pinterest.com/boldthemes/_created/', 'pinterest.com/')
    file.write_text(text, encoding='utf-8')
    count += 1
print(f'Filled fictional portfolio details in {count} pages.')
