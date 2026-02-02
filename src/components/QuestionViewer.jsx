import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function QuestionViewer() {
  const [exams, setExams] = useState([]);
  const [selectedExam, setSelectedExam] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [questionDetails, setQuestionDetails] = useState(null);
  const [loading, setLoading] = useState(false);

  // Cargar exámenes
  useEffect(() => {
    axios.get('http://localhost:3000/api/exams')
      .then(res => setExams(res.data))
      .catch(err => console.error('Error cargando exámenes:', err));
  }, []);

  // Cargar preguntas del examen seleccionado
  useEffect(() => {
    if (!selectedExam) return;

    setLoading(true);
    axios.get(`http://localhost:3000/api/exams/${selectedExam}/questions`)
      .then(res => {
        setQuestions(res.data);
        setSelectedQuestion(null);
        setQuestionDetails(null);
      })
      .catch(err => console.error('Error cargando preguntas:', err))
      .finally(() => setLoading(false));
  }, [selectedExam]);

  // Cargar detalles de la pregunta
  useEffect(() => {
    if (!selectedQuestion) return;

    setLoading(true);
    axios.get(`http://localhost:3000/api/questions/${selectedQuestion}`)
      .then(res => setQuestionDetails(res.data))
      .catch(err => console.error('Error cargando pregunta:', err))
      .finally(() => setLoading(false));
  }, [selectedQuestion]);

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-green-700 mb-8">
        🧬 Preguntas PAU Biología 2025
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* PANEL IZQUIERDO: Exámenes */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-green-700 mb-4">
              📋 Exámenes
            </h2>

            <div className="space-y-2">
              {exams.map(exam => (
                <button
                  key={exam.id}
                  onClick={() => setSelectedExam(exam.id)}
                  className={`w-full text-left px-4 py-3 rounded-lg font-semibold transition ${
                    selectedExam === exam.id
                      ? 'bg-green-700 text-white'
                      : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                >
                  Examen {exam.exam_letter}
                  <span className="text-sm block opacity-75">
                    {exam.total_questions} preguntas
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* PANEL CENTRAL: Preguntas */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-green-700 mb-4">
              ❓ Preguntas
            </h2>

            {loading && <p className="text-gray-500">Cargando...</p>}

            {!selectedExam && (
              <p className="text-gray-500">Selecciona un examen</p>
            )}

            {selectedExam && (
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {questions.map(q => (
                  <button
                    key={q.id}
                    onClick={() => setSelectedQuestion(q.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg text-sm transition ${
                      selectedQuestion === q.id
                        ? 'bg-green-700 text-white'
                        : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                  >
                    <strong>P{q.question_number}</strong>
                    <span className="ml-2 text-xs px-2 py-1 bg-opacity-20 bg-gray-500 rounded">
                      {q.bloque}
                    </span>
                    <div className="text-xs opacity-75 mt-1">
                      {q.total_points} pts
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* PANEL DERECHO: Detalles */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-green-700 mb-4">
              📖 Pregunta
            </h2>

            {loading && <p className="text-gray-500">Cargando...</p>}

            {!selectedQuestion && (
              <p className="text-gray-500">Selecciona una pregunta</p>
            )}

            {questionDetails && (
              <div className="space-y-4">
                {/* Enunciado */}
                <div>
                  <h3 className="font-bold text-lg mb-2">
                    Pregunta {questionDetails.question_number}
                  </h3>
                  <p className="text-sm text-gray-700">
                    {questionDetails.question_text}
                  </p>
                </div>

                {/* Imagen */}
                {questionDetails.image && (
                  <div className="border-2 border-green-200 rounded-lg p-3 bg-green-50">
                    <img
                      src={`http://localhost:3000${questionDetails.image.image_path}`}
                      alt={`Pregunta ${questionDetails.question_number}`}
                      className="w-full rounded h-auto"
                      onError={(e) => {
                        e.target.alt = '❌ Imagen no disponible';
                        e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23f0f0f0" width="100" height="100"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="%23999">Sin imagen</text></svg>';
                      }}
                    />
                  </div>
                )}

                {/* Apartados */}
                {questionDetails.apartados && questionDetails.apartados.length > 0 && (
                  <div>
                    <h4 className="font-bold text-sm mb-2">Apartados:</h4>
                    <div className="space-y-2">
                      {questionDetails.apartados.map((apt, idx) => (
                        <div key={idx} className="bg-gray-50 p-3 rounded text-sm">
                          <strong>{apt.apartado_letter})</strong> {apt.apartado_text}
                          <span className="block text-xs text-gray-500 mt-1">
                            {apt.points} pts
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Puntuación total */}
                <div className="border-t pt-3 mt-3">
                  <p className="text-sm">
                    <strong>Puntuación total:</strong> {questionDetails.total_points} pts
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
