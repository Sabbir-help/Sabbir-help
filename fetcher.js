// Topic: Web Development - API Interaction
// Repository: sabbir-help

async function getGithubUser(username) {
    try {
        const response = await fetch(`https://api.github.com/users/${username}`);
        const data = await response.json();
        console.log(`User: ${data.name}`);
        console.log(`Bio: ${data.bio}`);
        console.log(`Public Repos: ${data.public_repos}`);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

getGithubUser('sabbir-help');
