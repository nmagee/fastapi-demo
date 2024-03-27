let api = '/albums';

// Function to fetch data from the API
async function fetchData() {
    try {
        const response = await fetch(api);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to render data in cards
async function renderData() {
    const container = document.querySelector('.container');
    const data = await fetchData();

    if (!data) {
        return;
    }

    data.forEach(item => {
        const card = document.createElement('div');
        card.classList.add('card');

        const title = document.createElement('h2');
        title.textContent = item.name;

        const body = document.createElement('p');
        body.textContent = item.artist;

        const year = document.createElement('year');
        year.textContent = item.year + " / " + item.genre;

        card.appendChild(title);
        card.appendChild(body);
        card.appendChild(year);
        container.appendChild(card);
    });
}

// Call the renderData function to display data
renderData();

