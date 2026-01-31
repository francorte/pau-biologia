import axios from 'axios';

const API_BASE_URL = 'http://localhost:3000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Obtener estadísticas generales
  getStats: () => client.get('/stats'),
  
  // Obtener todos los exámenes
  getExams: () => client.get('/exams'),
  
  // Obtener examen por ID
  getExam: (examId) => client.get(`/exam/${examId}`),
  
  // Obtener pregunta completa con apartados
  getQuestion: (questionId) => client.get(`/question/${questionId}`),
  
  // Obtener bloques disponibles
  getBloques: () => client.get('/bloques'),
  
  // Obtener años disponibles
  getYears: () => client.get('/years'),
  
  // Health check
  health: () => client.get('/health'),
};

export default client;