import requests

# Your Hashnode API endpoint
HASHNODE_API_URL = "https://api.hashnode.com/"

# GraphQL query to fetch the latest 4 blog posts
query = """
{
  user(username: "thewoodhere") {
    publication {
      posts(page: 0, limit: 4) {
        title
        slug
        dateAdded
      }
    }
  }
}
"""

headers = {
    "Content-Type": "application/json",
}

# Make the request to Hashnode's API
response = requests.post(
    HASHNODE_API_URL,
    json={"query": query},
    headers=headers
)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    posts = data["data"]["user"]["publication"]["posts"]

    # Extract post titles and links
    blog_posts = [
        f"- [{post['title']}]({{'https://thewood.hashnode.dev/{post['slug']}'}})"
        for post in posts
    ]

    # Read the README file
    with open("README.md", "r") as file:
        readme_content = file.readlines()

    # Find the placeholder for blog posts and replace it
    start_index = readme_content.index("<!-- BLOG-POST-LIST:START -->\n")
    end_index = readme_content.index("<!-- BLOG-POST-LIST:END -->\n")

    # Replace the placeholder with the actual blog posts
    readme_content = (
        readme_content[:start_index + 1]
        + "\n".join(blog_posts)
        + "\n"
        + readme_content[end_index:]
    )

    # Write the updated README back
    with open("README.md", "w") as file:
        file.writelines(readme_content)

    print("README.md updated successfully!")
else:
    print("Failed to fetch blog posts:", response.status_code)
