import { useEffect, useState } from 'react';
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:3000/api',
});

export default function App() {
  const [exams, setExams] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [answers, setAnswers] = useState({});
  const [images, setImages] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [examsRes, statsRes] = await Promise.all([
        API.get('/exams'),
        API.get('/stats'),
      ]);
      // Filtrar SOLO 2025
      const exams2025 = examsRes.data.filter(exam => exam.year === 2025);
      setExams(exams2025);
      setStats(statsRes.data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExamClick = async (examId) => {
    try {
      const res = await API.get(`/exam/${examId}`);
      const questions = res.data.questions || [];
      if (questions.length > 0) {
        const detailRes = await API.get(`/question/${questions[0].id}`);
        setSelectedQuestion(detailRes.data);
        setAnswers({});
        
        // Cargar imágenes del examen
        try {
          const imagesRes = await API.get(`/images/${examId}`);
          setImages(imagesRes.data || []);
          console.log(`✓ ${imagesRes.data.length} imágenes cargadas`);
        } catch (err) {
          console.log('No hay imágenes disponibles');
          setImages([]);
        }
      }
    } catch (err) {
      console.error('Error:', err);
    }
  };

  const handleAnswerChange = (apartadoId, value) => {
    setAnswers((prev) => ({
      ...prev,
      [apartadoId]: value,
    }));
  };

  const handleSubmit = () => {
    console.log('Respuestas:', answers);
    alert('✅ Respuestas guardadas. Próximamente se evaluarán automáticamente.');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-green-50 to-emerald-50">
        <div className="text-center">
          <div className="text-6xl mb-4">🧬</div>
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-lg text-green-700 font-semibold">Cargando banco de preguntas 2025...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-green-600 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center gap-4 mb-3">
            <div className="text-5xl">🧬</div>
            <div>
              <h1 className="text-4xl font-bold text-green-900">PAU Biología</h1>
              <p className="text-green-600 font-semibold mt-1">
                Preguntas de examen. Entrenamiento para sacar la máxima nota en Selectividad
              </p>
              <p className="text-sm text-green-500 mt-1">📅 Año 2025</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-10">
        {error && (
          <div className="bg-red-50 border-2 border-red-300 text-red-800 px-6 py-4 rounded-xl mb-8 shadow-md">
            <p className="font-bold text-lg mb-2">⚠️ Error de conexión</p>
            <p className="mb-3">{error}</p>
            <button 
              onClick={loadData} 
              className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 font-semibold transition"
            >
              🔄 Reintentar
            </button>
          </div>
        )}

        {/* Statistics Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
            <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-8 text-white">
              <p className="text-green-100 text-sm font-semibold uppercase tracking-wide">Exámenes 2025</p>
              <p className="text-5xl font-bold mt-3">{exams.length}</p>
              <p className="text-green-100 text-sm mt-2">disponibles</p>
            </div>
            <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl shadow-lg p-8 text-white">
              <p className="text-emerald-100 text-sm font-semibold uppercase tracking-wide">Preguntas Totales</p>
              <p className="text-5xl font-bold mt-3">{stats.total_questions}</p>
              <p className="text-emerald-100 text-sm mt-2">en BD</p>
            </div>
            <div className="bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl shadow-lg p-8 text-white">
              <p className="text-teal-100 text-sm font-semibold uppercase tracking-wide">Apartados</p>
              <p className="text-5xl font-bold mt-3">{stats.total_apartados}</p>
              <p className="text-teal-100 text-sm mt-2">subpreguntas</p>
            </div>
            <div className="bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl shadow-lg p-8 text-white">
              <p className="text-blue-100 text-sm font-semibold uppercase tracking-wide">Imágenes</p>
              <p className="text-5xl font-bold mt-3">{stats.total_images}</p>
              <p className="text-blue-100 text-sm mt-2">figuras</p>
            </div>
          </div>
        )}

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Exams Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-7 sticky top-24 border-t-4 border-green-600">
              <h2 className="text-2xl font-bold text-green-900 mb-6 flex items-center gap-2">
                📋 Exámenes 2025
              </h2>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {exams.length === 0 ? (
                  <p className="text-gray-500 text-center py-8 font-semibold">
                    No hay exámenes en 2025
                  </p>
                ) : (
                  exams.map((exam) => (
                    <button
                      key={exam.id}
                      onClick={() => handleExamClick(exam.id)}
                      className="w-full text-left px-5 py-4 bg-gradient-to-r from-green-50 to-emerald-50 hover:from-green-100 hover:to-emerald-100 rounded-lg border-2 border-green-200 hover:border-green-400 transition font-medium"
                    >
                      <p className="font-bold text-green-900">📅 Examen {exam.exam_letter}</p>
                      <p className="text-xs text-green-600 mt-1">{exam.id}</p>
                    </button>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Question Detail */}
          <div className="lg:col-span-2">
            {selectedQuestion ? (
              <div className="bg-white rounded-xl shadow-lg p-10 border-t-4 border-green-600 overflow-y-auto max-h-screen">
                {/* Question Header */}
                <div className="mb-10 pb-8 border-b-3 border-green-200">
                  <div className="flex items-center gap-3 mb-4 flex-wrap">
                    <span className="inline-block px-4 py-2 bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 rounded-full text-sm font-bold border-2 border-green-300">
                      🧬 Bloque {selectedQuestion.question?.bloque}
                    </span>
                    <span className="text-green-700 text-sm font-semibold">
                      {selectedQuestion.question?.year} · Examen {selectedQuestion.question?.exam_letter}
                    </span>
                  </div>
                  <h2 className="text-3xl font-bold text-green-900">
                    Pregunta {selectedQuestion.question?.question_number}
                  </h2>
                </div>

                {/* Imágenes */}
                {images.length > 0 && (
                  <div className="mb-10">
                    <h3 className="text-xl font-bold text-green-900 mb-5 flex items-center gap-2">
                      🖼️ Figuras ({images.length})
                    </h3>
                    <div className="grid grid-cols-1 gap-6">
                      {images.map((img) => (
                        <div key={img.id} className="bg-gray-100 p-4 rounded-lg border-2 border-gray-300">
                          <p className="text-sm text-gray-600 mb-3 font-semibold">Página {img.page_number}</p>
                          {img.image_data && (
                            <img 
                              src={`data:image/png;base64,${img.image_data}`}
                              alt={`Figura página ${img.page_number}`}
                              className="w-full rounded-lg border-2 border-gray-400 max-h-96 object-contain"
                            />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Enunciado */}
                <div className="mb-10">
                  <h3 className="text-xl font-bold text-green-900 mb-5 flex items-center gap-2">
                    📝 Enunciado
                  </h3>
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 p-8 rounded-lg leading-relaxed text-gray-800 font-medium whitespace-pre-wrap">
                    {selectedQuestion.question?.text}
                  </div>
                </div>

                {/* Apartados */}
                <div className="mb-10">
                  <h3 className="text-xl font-bold text-green-900 mb-6 flex items-center gap-2">
                    ✏️ Apartados ({selectedQuestion.apartados?.length})
                  </h3>
                  <div className="space-y-6">
                    {selectedQuestion.apartados?.map((apartado) => (
                      <div 
                        key={apartado.id} 
                        className="border-l-4 border-green-500 bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-lg hover:shadow-md transition"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <label className="text-lg font-bold text-green-900">
                            {apartado.label})
                          </label>
                          <span className="inline-block bg-gradient-to-r from-yellow-400 to-yellow-500 text-yellow-900 text-xs font-bold px-3 py-1 rounded-full">
                            {apartado.points} pts
                          </span>
                        </div>
                        <p className="text-gray-700 mb-5 font-medium whitespace-pre-wrap">{apartado.text}</p>
                        <textarea
                          value={answers[apartado.id] || ''}
                          onChange={(e) => handleAnswerChange(apartado.id, e.target.value)}
                          placeholder="Escribe tu respuesta aquí..."
                          className="w-full px-4 py-3 border-2 border-green-300 rounded-lg focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 resize-none font-medium text-gray-800"
                          rows="4"
                        />
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 pt-8 border-t-3 border-green-200">
                  <button
                    onClick={handleSubmit}
                    className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-bold py-3 rounded-lg hover:from-green-700 hover:to-emerald-700 transition shadow-lg text-lg"
                  >
                    ✅ Guardar Respuestas
                  </button>
                  <button
                    onClick={() => setAnswers({})}
                    className="flex-1 bg-gray-300 text-gray-800 font-bold py-3 rounded-lg hover:bg-gray-400 transition shadow-lg text-lg"
                  >
                    🔄 Limpiar
                  </button>
                </div>

                {/* Info Box */}
                <div className="mt-8 bg-gradient-to-r from-blue-50 to-cyan-50 border-2 border-blue-300 text-blue-900 px-6 py-4 rounded-lg">
                  <p className="font-semibold">ℹ️ Próximamente:</p>
                  <p className="text-sm mt-2">
                    Las respuestas se evaluarán automáticamente usando criterios oficiales PAU. 
                    Recibirás feedback detallado y sugerencias de mejora.
                  </p>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-lg p-12 text-center h-96 flex items-center justify-center border-t-4 border-green-600">
                <div>
                  <div className="text-6xl mb-4">👈</div>
                  <p className="text-2xl font-bold text-green-900 mb-2">Selecciona un examen</p>
                  <p className="text-gray-600 font-medium">para comenzar a practicar</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-green-900 text-white mt-16 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="font-semibold">🧬 PAU Biología · Plataforma de Entrenamiento 2025</p>
          <p className="text-green-200 text-sm mt-2">Diseñada para alcanzar la máxima nota en Selectividad</p>
        </div>
      </footer>
    </div>
  );
}