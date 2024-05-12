// script.js
document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    const productName = document.getElementById('product-name').value.trim();
    if (productName !== '') {
        searchProducts(productName);
    }
});

function searchProducts(productName) {
    fetch(`/search?product_name=${productName}`)
        .then(response => response.json())
        .then(data => {
            displayProductInfo(data.amazon_info, 'amazon-results');
            displayProductInfo(data.flipkart_info, 'flipkart-results');
        })
        .catch(error => console.error('Error searching products:', error));
}

function displayProductInfo(productInfo, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    if (productInfo) {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product-info');
        const titleHeading = document.createElement('h2');
        titleHeading.textContent = productInfo.title;
        const priceParagraph = document.createElement('p');
        priceParagraph.textContent = `Price: ${productInfo.price}`;
        const ratingParagraph = document.createElement('p');
        ratingParagraph.textContent = `Rating: ${productInfo.rating}`;
        
        productDiv.appendChild(titleHeading);
        productDiv.appendChild(priceParagraph);
        productDiv.appendChild(ratingParagraph);
        container.appendChild(productDiv);
    } else {
        const notFoundDiv = document.createElement('div');
        notFoundDiv.classList.add('product-info');
        notFoundDiv.classList.add('not-found');
        notFoundDiv.textContent = 'Product not found';
        container.appendChild(notFoundDiv);
    }
}
