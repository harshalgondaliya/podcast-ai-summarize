import streamlit as st
import json
import os
import base64
import feedparser
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import time

def main():
    # Set page config
    st.set_page_config(
        page_title="Podcast Summarizer",
        page_icon="🎙️",
        layout="wide"
    )

    # Simple title
    st.title("Podcast Summarizer")

    # Initialize session state for podcast info if not exists
    if 'available_podcast_info' not in st.session_state:
        st.session_state.available_podcast_info = create_dict_from_json_files('content')

    # Sidebar section
    with st.sidebar:
        st.header("Add New Podcast")
        url = st.text_input("Enter RSS Feed URL")
        process_button = st.button("Process Feed")

        if process_button and url:
            with st.spinner('Processing podcast feed...'):
                try:
                    if not urlparse(url).scheme:
                        url = 'https://' + url
                    
                    podcast_info = process_podcast_info(url)
                    
                    if podcast_info['podcast_summary'] and podcast_info['podcast_summary'] != "Error processing RSS feed":
                        new_podcast_name = get_next_available_name(st.session_state.available_podcast_info)
                        save_path = os.path.join('content', new_podcast_name)
                        with open(save_path, 'w') as json_file:
                            json.dump(podcast_info, json_file, indent=4)
                        
                        podcast_title = podcast_info['podcast_details']['podcast_title']
                        st.session_state.available_podcast_info[podcast_title] = podcast_info
                        st.success("Podcast processed successfully!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("Failed to process the podcast feed. Please check the URL and try again.")
                except Exception as e:
                    st.error(f"Error processing podcast: {str(e)}")

        st.header("Available Podcasts")
        if st.session_state.available_podcast_info:
            selected_podcast = st.selectbox(
                "Select a podcast",
                options=list(st.session_state.available_podcast_info.keys()),
                index=len(st.session_state.available_podcast_info) - 1 if st.session_state.available_podcast_info else 0
            )
        else:
            st.info("No podcasts available. Add a podcast feed to get started.")

    # Main content area
    if selected_podcast:
        podcast_info = st.session_state.available_podcast_info[selected_podcast]
        display_podcast_info(podcast_info)

def display_podcast_info(podcast_info):
    """Display podcast information in a structured format"""
    try:
        # Create two columns for title and image
        col1, col2 = st.columns([7, 3])

        with col1:
            # Podcast header with title and episode
            st.header(podcast_info['podcast_details']['podcast_title'])
            st.subheader(podcast_info['podcast_details']['episode_title'])

        with col2:
            # Handle image display with error handling
            image_url = podcast_info['podcast_details']['episode_image']
            if image_url and image_url.strip():
                try:
                    # Download the image
                    response = requests.get(image_url, stream=True)
                    if response.status_code == 200:
                        # Convert the image to bytes
                        image_bytes = response.content
                        # Display the image
                        st.image(image_bytes)
                    else:
                        st.warning("Could not load podcast image")
                except Exception as e:
                    st.warning(f"Error loading image: {str(e)}")

        # Summary
        st.subheader("Summary")
        if podcast_info['podcast_summary']:
            st.write(podcast_info['podcast_summary'])
        else:
            st.info("No summary available")

        # Guest information
        st.subheader("Guest Information")
        col3, col4 = st.columns([3, 7])

        with col3:
            guest_info = f"{podcast_info['podcast_guest']['name']}"
            if podcast_info['podcast_guest']['job']:
                guest_info += f", {podcast_info['podcast_guest']['job']}"
            
            guest_image = podcast_info['podcast_guest']['wiki_img']
            if guest_image and guest_image.strip():
                try:
                    st.image(guest_image, caption=guest_info)
                except Exception as e:
                    st.write(guest_info)
            else:
                st.write(guest_info)

        with col4:
            guest_details = []
            if podcast_info['podcast_guest']['wiki_title']:
                guest_details.append(podcast_info['podcast_guest']['wiki_title'])
            if podcast_info['podcast_guest']['wiki_summary']:
                guest_details.append(podcast_info['podcast_guest']['wiki_summary'])
            if podcast_info['podcast_guest']['wiki_url']:
                guest_details.append(f"[Wikipedia Link]({podcast_info['podcast_guest']['wiki_url']})")
            if podcast_info['podcast_guest']['google_URL']:
                guest_details.append(f"[Google Search]({podcast_info['podcast_guest']['google_URL']})")
            
            if guest_details:
                st.write("\n\n".join(guest_details))
            else:
                st.info("No additional guest details available")

        # Key moments
        st.subheader("Key Moments")
        if podcast_info['podcast_highlights']:
            highlights = podcast_info['podcast_highlights'].split('\n')
            for highlight in highlights:
                if highlight.strip():
                    st.write(f"• {highlight.strip()}")
        else:
            st.info("No key moments available")

    except Exception as e:
        st.error(f"Error displaying podcast information: {str(e)}")

def process_podcast_info(url):
    """Process RSS feed and extract podcast information"""
    try:
        # Parse the RSS feed
        feed = feedparser.parse(url)
        
        if not feed.entries:
            return create_error_response("No episodes found in the RSS feed. Please check the URL and try again.")

        # Get the latest episode
        latest_episode = feed.entries[0]
        
        # Extract basic information
        episode_title = latest_episode.get('title', 'No title available')
        episode_description = latest_episode.get('description', 'No description available')
        
        # Extract podcast name - try multiple sources
        podcast_title = ''
        
        # First try to get the podcast title from the feed
        if hasattr(feed.feed, 'title'):
            podcast_title = feed.feed.title
        elif hasattr(feed.feed, 'itunes_title'):
            podcast_title = feed.feed.itunes_title
        elif hasattr(feed.feed, 'subtitle'):
            podcast_title = feed.feed.subtitle
        
        # Clean up the podcast title
        if podcast_title:
            # Remove common suffixes and prefixes
            podcast_title = re.sub(r'^\s*The\s+', '', podcast_title, flags=re.IGNORECASE)
            podcast_title = re.sub(r'\s*-\s*Podcast$', '', podcast_title, flags=re.IGNORECASE)
            podcast_title = re.sub(r'\s*Podcast$', '', podcast_title, flags=re.IGNORECASE)
            podcast_title = re.sub(r'\s*Show$', '', podcast_title, flags=re.IGNORECASE)
            podcast_title = re.sub(r'\s*Series$', '', podcast_title, flags=re.IGNORECASE)
            # Remove any HTML tags
            podcast_title = re.sub(r'<[^>]+>', '', podcast_title)
            # Clean up whitespace
            podcast_title = ' '.join(podcast_title.split())
        
        # If we still don't have a podcast title, try to extract it from the episode title
        if not podcast_title and episode_title:
            # Common patterns to try
            patterns = [
                r'^([^:]+):\s*(.+)$',  # "Podcast: Episode"
                r'^([^-]+)\s*-\s*(.+)$',  # "Podcast - Episode"
                r'^([^|]+)\s*\|\s*(.+)$',  # "Podcast | Episode"
                r'^([^(]+)\s*\((.+)\)$',  # "Podcast (Episode)"
                r'^(.+?)\s*Episode\s+\d+:\s*(.+)$',  # "Podcast Episode 123: Title"
                r'^(.+?)\s*#\d+:\s*(.+)$'  # "Podcast #123: Title"
            ]
            
            for pattern in patterns:
                match = re.match(pattern, episode_title, re.IGNORECASE)
                if match:
                    podcast_title = match.group(1).strip()
                    episode_title = match.group(2).strip()
                    break
            
            # If no pattern matched, try to find the podcast name in the episode title
            if not podcast_title:
                words = episode_title.split()
                if len(words) > 2:
                    # Try to find a natural break in the title
                    for i in range(2, len(words)):
                        if words[i][0].isupper() and i > 1:
                            podcast_title = ' '.join(words[:i])
                            episode_title = ' '.join(words[i:])
                            break
                    else:
                        podcast_title = ' '.join(words[:2])
        
        # Extract image
        episode_image = extract_image_url(latest_episode)
        
        # Process content
        summary, highlights = process_content(episode_description)
        
        # Extract guest information
        guest_info = extract_guest_info(episode_title, episode_description)
        
        return {
            "podcast_summary": summary,
            "podcast_highlights": highlights,
            "podcast_details": {
                "podcast_title": podcast_title or "Unknown Podcast",
                "episode_title": episode_title,
                "episode_image": episode_image
            },
            "podcast_guest": guest_info
        }
    
    except Exception as e:
        return create_error_response(f"Error processing RSS feed: {str(e)}")

def extract_image_url(episode):
    """Extract image URL from episode data"""
    # Try different methods to get the image URL
    image_url = ''
    
    # Method 1: Check episode.image
    if hasattr(episode, 'image') and episode.image:
        if hasattr(episode.image, 'href'):
            image_url = episode.image.href
        elif hasattr(episode.image, 'url'):
            image_url = episode.image.url
    
    # Method 2: Check media_content
    if not image_url and hasattr(episode, 'media_content'):
        for media in episode.media_content:
            if media.get('type', '').startswith('image'):
                image_url = media.get('url', '')
                if image_url:
                    break
    
    # Method 3: Check itunes_image
    if not image_url and hasattr(episode, 'itunes_image'):
        if hasattr(episode.itunes_image, 'href'):
            image_url = episode.itunes_image.href
    
    # Method 4: Check enclosure
    if not image_url and hasattr(episode, 'enclosures'):
        for enclosure in episode.enclosures:
            if enclosure.get('type', '').startswith('image'):
                image_url = enclosure.get('url', '')
                if image_url:
                    break
    
    # Method 5: Check feed image
    if not image_url and hasattr(episode, 'feed'):
        if hasattr(episode.feed, 'image'):
            if hasattr(episode.feed.image, 'href'):
                image_url = episode.feed.image.href
            elif hasattr(episode.feed.image, 'url'):
                image_url = episode.feed.image.url
    
    # Method 6: Check for image in content
    if not image_url and hasattr(episode, 'content'):
        for content in episode.content:
            soup = BeautifulSoup(content.value, 'html.parser')
            img = soup.find('img')
            if img and img.get('src'):
                image_url = img['src']
                break
    
    # Method 7: Check for image in description
    if not image_url and hasattr(episode, 'description'):
        soup = BeautifulSoup(episode.description, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            image_url = img['src']
    
    # Validate the URL
    if image_url:
        # Ensure URL has proper scheme
        if not image_url.startswith(('http://', 'https://')):
            image_url = 'https://' + image_url
        
        # Try to verify the image URL
        try:
            response = requests.head(image_url, timeout=5)
            if response.status_code != 200:
                image_url = ''
        except:
            image_url = ''
    
    return image_url

def process_content(description):
    """Process episode description to extract summary and highlights"""
    soup = BeautifulSoup(description, 'html.parser')
    
    # Remove unwanted tags
    for tag in soup.find_all(['script', 'style', 'iframe', 'a']):
        tag.decompose()
    
    # Get all paragraphs
    paragraphs = soup.find_all(['p', 'div'])
    
    # Extract summary
    summary_parts = []
    for p in paragraphs:
        text = p.get_text().strip()
        if text and len(text) > 20:
            text = re.sub(r'\s+', ' ', text)
            summary_parts.append(text)
    
    # If no paragraphs found, try raw text
    if not summary_parts:
        raw_text = re.sub(r'<[^>]+>', ' ', description)
        raw_text = re.sub(r'\s+', ' ', raw_text).strip()
        if raw_text:
            summary_parts = [raw_text]
    
    summary = ' '.join(summary_parts[:3])
    if len(summary) > 500:
        summary = summary[:500] + "..."
    
    # Extract highlights
    highlights = []
    for i, p in enumerate(paragraphs[:5], 1):
        text = p.get_text().strip()
        if text and len(text) > 20:
            text = re.sub(r'\s+', ' ', text)
            timestamp_match = re.search(r'(\d{1,2}:\d{2})', text)
            if timestamp_match:
                timestamp = timestamp_match.group(1)
                text = f"{timestamp} - {text}"
            highlights.append(f"{i}. {text}")
    
    # If no highlights, create from summary
    if not highlights and summary:
        summary_sentences = re.split(r'(?<=[.!?])\s+', summary)
        for i, sentence in enumerate(summary_sentences[:5], 1):
            if len(sentence) > 20:
                highlights.append(f"{i}. {sentence}")
    
    return summary, "\n".join(highlights)

def extract_guest_info(title, description):
    """Extract guest information from title and description"""
    guest_name = "Guest information not available"
    guest_job = ""
    
    # Try to extract from title
    title_text = title.lower()
    if "with" in title_text:
        parts = title_text.split("with")
        if len(parts) > 1:
            guest_info = parts[1].strip()
            if "about" in guest_info:
                guest_info = guest_info.split("about")[0].strip()
            guest_name = guest_info.title()
    
    # Try to extract from description
    if guest_name == "Guest information not available":
        soup = BeautifulSoup(description, 'html.parser')
        for p in soup.find_all(['p', 'div']):
            text = p.get_text().lower()
            if "guest" in text or "speaker" in text or "host" in text:
                match = re.search(r'(?:guest|speaker|host)[:\s]+([^.,]+)', text)
                if match:
                    guest_name = match.group(1).strip().title()
                    break
    
    return {
        "name": guest_name,
        "job": guest_job,
        "wiki_img": "",
        "wiki_title": "",
        "wiki_summary": "",
        "wiki_url": "",
        "google_URL": ""
    }

def create_error_response(error_message):
    """Create an error response dictionary"""
    return {
        "podcast_summary": error_message,
        "podcast_highlights": "",
        "podcast_details": {
            "podcast_title": "Error",
            "episode_title": "Error processing feed",
            "episode_image": ""
        },
        "podcast_guest": {
            "name": "",
            "job": "",
            "wiki_img": "",
            "wiki_title": "",
            "wiki_summary": "",
            "wiki_url": "",
            "google_URL": ""
        }
    }

def create_dict_from_json_files(folder_path):
    """Create a dictionary from JSON files in the specified folder"""
    data_dict = {}
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(folder_path, file_name)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        # Use the podcast title as the key instead of the filename
                        podcast_title = data.get('podcast_details', {}).get('podcast_title', file_name)
                        data_dict[podcast_title] = data
                except Exception as e:
                    print(f"Error loading {file_name}: {str(e)}")
    return data_dict

def get_next_available_name(existing_podcasts):
    """Generate the next available name for a new podcast"""
    idx = len(existing_podcasts) + 1
    return f"podcast-{idx}.json"

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    """Convert binary file to base64"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    """Set PNG image as page background"""
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    opacity: 0.8;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
