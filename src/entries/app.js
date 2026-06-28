import '../stylesheets/styles.css'; 
import '../stylesheets/dashboard.css'; 
import { AutoComplete } from '../plugins/AutoComplete.js';
import '../plugins/AutoComplete.css';
import { FileUpload } from '../plugins/FileUpload.js';
import '../plugins/FileUpload.css';

window.AutoComplete = AutoComplete;
window.FileUpload = FileUpload;

const fetchTokensIfMissing = () => {
  const hasFilesToken = localStorage.getItem('jwtFilesToken');
  const hasAccessToken = localStorage.getItem('jwtAccessToken');
  const hasChatToken = localStorage.getItem('jwtChatToken');

  if (hasFilesToken && hasAccessToken && hasChatToken) {
    console.log('Tokens ya existen en localStorage.');
    return Promise.resolve();
  }

  return fetch('/api/v1/session', {
    method: 'GET',
    credentials: 'include'
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return response.json();
    })
    .then((res) => {
      const data = res.data; // 👈 importante
      const tokens = data?.tokens;
      const user = data?.user;

      // 🔐 tokens corregidos según tu JSON
      if (tokens?.access) {
        localStorage.setItem('jwtAccessToken', tokens.access);
      }

      if (tokens?.file) {
        localStorage.setItem('jwtFilesToken', tokens.file);
      }

      // ⚠️ no veo chat token en tu JSON actual
      // si existe en backend luego, sería algo como:
      // if (tokens?.chat) localStorage.setItem('jwtChatToken', tokens.chat);

      // 👤 user
      if (user) {
        localStorage.setItem('user_info', JSON.stringify(user));
      }

      console.log('Tokens guardados en localStorage.');
    })
    .catch((error) => {
      console.error('Error al obtener tokens:', error);
      return Promise.reject(error);
    });
};

document.addEventListener('DOMContentLoaded', function() {
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  
  let isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
  
  function updateSidebarState() {
    if (window.innerWidth <= 992) {
      sidebar.classList.add('collapsed');
    } else {
      sidebar.classList.toggle('collapsed', isCollapsed);
    }
  }
  
  updateSidebarState();
  
  sidebarToggle.addEventListener('click', function() {
    if (window.innerWidth <= 992) {
      sidebar.classList.toggle('collapsed');
    } else {
      isCollapsed = !isCollapsed;
      localStorage.setItem('sidebarCollapsed', isCollapsed);
      sidebar.classList.toggle('collapsed');
    }
  });
  
  document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    link.addEventListener('click', function() {
      if (window.innerWidth <= 992) {
        sidebar.classList.add('collapsed');
      }
    });
  });
  
  window.addEventListener('resize', function() {
    updateSidebarState();
  });

  // tokens de servicios
  fetchTokensIfMissing()
  .then(() => {
    console.log('Tokens listos para usar.');
  })
  .catch(err => {
    console.error('No se pudieron obtener los tokens:', err);
  });
});