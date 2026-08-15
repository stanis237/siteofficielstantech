/* ==========================================================================
   STANTECH - Main JavaScript Controller
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initCartDrawer();
  initQuickViewModal();
  initShopFilters();
  initCheckoutForm();
});

// Helper: Get CSRF Token
function getCsrfToken() {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Toast Notification
function showToast(message, icon = 'check-circle') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<i data-lucide="${icon}"></i> <span>${message}</span>`;
  container.appendChild(toast);
  
  if (window.lucide) {
    lucide.createIcons();
  }

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.className = 'toast-container';
  document.body.appendChild(container);
  return container;
}

// Navbar Scroll & Mobile Toggle
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  const mobileToggle = document.querySelector('.mobile-toggle');
  const navMenu = document.querySelector('.nav-menu');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
    });
  }
}

// Cart Drawer
function initCartDrawer() {
  const cartTrigger = document.querySelector('.cart-trigger');
  const cartOverlay = document.querySelector('.cart-drawer-overlay');
  const cartCloseBtn = document.querySelector('.cart-close-btn');

  if (cartTrigger && cartOverlay) {
    cartTrigger.addEventListener('click', () => {
      cartOverlay.classList.add('active');
    });
  }

  if (cartCloseBtn && cartOverlay) {
    cartCloseBtn.addEventListener('click', () => {
      cartOverlay.classList.remove('active');
    });
  }

  if (cartOverlay) {
    cartOverlay.addEventListener('click', (e) => {
      if (e.target === cartOverlay) {
        cartOverlay.classList.remove('active');
      }
    });
  }
}

// Add To Cart AJAX
function addToCart(productId, quantity = 1) {
  fetch('/api/cart/add/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({ product_id: productId, quantity: quantity })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      updateCartUI(data);
      showToast(data.message || 'Produit ajouté au panier !');
      // Open drawer
      const cartOverlay = document.querySelector('.cart-drawer-overlay');
      if (cartOverlay) cartOverlay.classList.add('active');
    } else {
      showToast(data.message || 'Erreur lors de l\'ajout', 'alert-circle');
    }
  })
  .catch(err => {
    console.error(err);
    showToast('Erreur de connexion au serveur', 'alert-circle');
  });
}

// Update Cart Quantity AJAX
function updateCartQuantity(productId, quantity) {
  fetch('/api/cart/update/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({ product_id: productId, quantity: quantity })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      updateCartUI(data);
    }
  });
}

// Update Cart UI Elements
function updateCartUI(data) {
  // Update badges
  const cartCounts = document.querySelectorAll('.cart-count');
  cartCounts.forEach(el => el.textContent = data.cart_count);

  // Update Drawer Items
  const cartBody = document.querySelector('.cart-body');
  const cartTotalEl = document.querySelector('.cart-drawer-total');

  if (cartTotalEl) {
    cartTotalEl.textContent = new Intl.NumberFormat('fr-FR').format(data.cart_total) + ' FCFA';
  }

  if (cartBody) {
    if (data.cart_count === 0) {
      cartBody.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem; color: #64748b;">
          <i data-lucide="shopping-bag" style="width: 48px; height: 48px; margin-bottom: 1rem; color: #94a3b8;"></i>
          <p>Votre panier est vide</p>
        </div>
      `;
    } else {
      let html = '';
      for (const [id, item] of Object.entries(data.cart_items)) {
        html += `
          <div class="cart-item">
            <img src="${item.image_url || '/static/images/placeholder.jpg'}" class="cart-item-img" alt="${item.name}">
            <div class="cart-item-details">
              <div class="cart-item-title">${item.name}</div>
              <div class="cart-item-price">${new Intl.NumberFormat('fr-FR').format(item.price)} FCFA</div>
              <div class="cart-item-qty">
                <button class="qty-btn" onclick="updateCartQuantity('${id}', ${item.quantity - 1})">-</button>
                <span>${item.quantity}</span>
                <button class="qty-btn" onclick="updateCartQuantity('${id}', ${item.quantity + 1})">+</button>
                <button style="margin-left: auto; background: none; border: none; color: #ef4444; cursor: pointer;" onclick="updateCartQuantity('${id}', 0)">
                  <i data-lucide="trash-2" style="width: 16px; height: 16px;"></i>
                </button>
              </div>
            </div>
          </div>
        `;
      }
      cartBody.innerHTML = html;
    }
    if (window.lucide) lucide.createIcons();
  }
}

// Shop Search & Category Filtering
function initShopFilters() {
  const searchInput = document.getElementById('shop-search');
  const categoryFilterBtns = document.querySelectorAll('.category-filter-btn');
  const productCards = document.querySelectorAll('.product-card');

  if (!productCards.length) return;

  let currentCategory = 'all';

  function filterProducts() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

    productCards.forEach(card => {
      const title = card.getAttribute('data-name') ? card.getAttribute('data-name').toLowerCase() : '';
      const category = card.getAttribute('data-category') || '';
      
      const matchesSearch = title.includes(query);
      const matchesCategory = (currentCategory === 'all' || category === currentCategory);

      if (matchesSearch && matchesCategory) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', filterProducts);
  }

  categoryFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      categoryFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.getAttribute('data-category');
      filterProducts();
    });
  });
}

// Quick View Modal
function initQuickViewModal() {
  const modalOverlay = document.getElementById('quickview-modal');
  const modalCloseBtn = modalOverlay ? modalOverlay.querySelector('.modal-close') : null;

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', () => modalOverlay.classList.remove('active'));
  }
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) modalOverlay.classList.remove('active');
    });
  }
}

function openQuickView(productId) {
  fetch(`/api/product/${productId}/`)
    .then(res => res.json())
    .then(product => {
      const modalOverlay = document.getElementById('quickview-modal');
      const modalBody = modalOverlay.querySelector('.modal-body-content');

      if (modalBody) {
        modalBody.innerHTML = `
          <div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 2rem;">
            <div>
              <img src="${product.image_url}" style="width: 100%; border-radius: 12px; height: 280px; object-fit: cover;" alt="${product.name}">
            </div>
            <div>
              <span class="badge badge-primary">${product.category_name}</span>
              <h2 style="font-size: 1.6rem; margin: 0.6rem 0;">${product.name}</h2>
              <div style="font-size: 1.4rem; font-weight: 800; color: #059669; margin-bottom: 1rem;">
                ${new Intl.NumberFormat('fr-FR').format(product.price)} FCFA
              </div>
              <p style="color: #64748b; margin-bottom: 1.5rem; font-size: 0.95rem;">${product.short_description}</p>
              
              <div style="margin-bottom: 1.5rem;">
                <strong>Spécifications clés :</strong>
                <ul style="margin-top: 0.5rem; padding-left: 1.2rem; color: #334155; font-size: 0.9rem;">
                  ${product.specs ? product.specs.split('\n').map(s => `<li>${s}</li>`).join('') : '<li>Matériel de qualité STANTECH</li>'}
                </ul>
              </div>

              <button class="btn btn-primary" style="width: 100%;" onclick="addToCart('${product.id}'); document.getElementById('quickview-modal').classList.remove('active');">
                <i data-lucide="shopping-cart"></i> Ajouter au Panier
              </button>
            </div>
          </div>
        `;
        if (window.lucide) lucide.createIcons();
      }
      modalOverlay.classList.add('active');
    });
}

// Checkout Form Modal / Processing
function openCheckoutModal() {
  const cartOverlay = document.querySelector('.cart-drawer-overlay');
  if (cartOverlay) cartOverlay.classList.remove('active');

  const checkoutModal = document.getElementById('checkout-modal');
  if (checkoutModal) {
    checkoutModal.classList.add('active');
  }
}

function initCheckoutForm() {
  const form = document.getElementById('checkout-form');
  const checkoutModal = document.getElementById('checkout-modal');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());

      fetch('/api/checkout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(data)
      })
      .then(res => res.json())
      .then(res => {
        if (res.success) {
          if (checkoutModal) checkoutModal.classList.remove('active');
          showToast(`Commande ${res.order_number} validée avec succès !`, 'check-circle');
          updateCartUI(res);
          // Show order success modal instead of alert
          const successOverlay = document.createElement('div');
          successOverlay.className = 'modal-overlay active';
          successOverlay.style.zIndex = '99999';
          successOverlay.innerHTML = `
            <div class="modal-content" style="max-width: 500px; text-align: center; padding: 3rem 2rem;">
              <div style="width: 80px; height: 80px; background: #d1fae5; color: #059669; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem;">
                <i data-lucide="check-circle" style="width: 40px; height: 40px;"></i>
              </div>
              <h2 style="font-size: 1.8rem; margin-bottom: 1rem; color: #0f172a;">Succès !</h2>
              <p style="color: #475569; font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">
                Votre commande N° <strong>${res.order_number}</strong> a été enregistrée chez STANTECH avec succès.<br><br>
                Notre équipe va prendre contact avec vous sous peu pour la livraison.
              </p>
              <button class="btn btn-primary" onclick="this.closest('.modal-overlay').remove()" style="padding: 0.8rem 2rem; width: 100%;">Fermer</button>
            </div>
          `;
          document.body.appendChild(successOverlay);
          if (window.lucide) lucide.createIcons();
        } else {
          showToast(res.message || 'Erreur lors de la commande', 'alert-circle');
        }
      });
    });
  }
}
