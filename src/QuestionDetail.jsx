import { useState } from 'react';

export default function QuestionDetail({ question }) {
  const [answers, setAnswers] = useState({});

  if (!question) {
    return null;
  }

  const handleAnswerChange = (apartadoId, value) => {
    setAnswers((prev) => ({
      ...prev,
      [apartadoId]: value,
    }));
  };

  const handleSubmit = () => {
    console.log('Respuestas:', answers);
    alert('Respuestas guardadas. (Próximamente se evaluarán automáticamente)');
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      {/* Header */}
      <div className="mb-8 pb-6 border-b-2 border-gray-200">
        <div className="flex items-center gap-3 mb-3">
          <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold">
            Bloque {question.question?.bloque || 'N/A'}
          </span>
          <span className="text-gray-500 text-sm">
            {question.question?.year} - Examen {question.question?.exam_letter}
          </span>
        </div>
        <h2 className="text-2xl font-bold text-gray-900">
          Pregunta {question.question?.question_number}
        </h2>
      </div>

      {/* Enunciado */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          📝 Enunciado
        </h3>
        <p className="text-gray-700 bg-gray-50 p-6 rounded-lg leading-relaxed">
          {question.question?.text || 'Sin enunciado'}
        </p>
      </div>

      {/* Apartados */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          ✏️ Apartados
        </h3>

        <div className="space-y-6">
          {question.apartados && question.apartados.length > 0 ? (
            question.apartados.map((apartado) => (
              <div
                key={apartado.id}
                className="border-l-4 border-blue-500 bg-blue-50 p-4 rounded"
              >
                <div className="flex items-start justify-between mb-2">
                  <label className="text-lg font-bold text-gray-900">
                    {apartado.label})
                  </label>
                  <span className="inline-block bg-yellow-100 text-yellow-800 text-xs font-semibold px-2 py-1 rounded">
                    {apartado.points} pts
                  </span>
                </div>

                <p className="text-gray-700 mb-4">{apartado.text}</p>

                <textarea
                  value={answers[apartado.id] || ''}
                  onChange={(e) =>
                    handleAnswerChange(apartado.id, e.target.value)
                  }
                  placeholder="Escribe tu respuesta aquí..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 resize-none"
                  rows="4"
                />
              </div>
            ))
          ) : (
            <p className="text-gray-500">No hay apartados disponibles</p>
          )}
        </div>
      </div>

      {/* Botones */}
      <div className="flex gap-4 pt-6 border-t border-gray-200">
        <button
          onClick={handleSubmit}
          className="flex-1 bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition"
        >
          ✅ Guardar Respuestas
        </button>
        <button
          onClick={() => setAnswers({})}
          className="flex-1 bg-gray-300 text-gray-700 font-semibold py-3 rounded-lg hover:bg-gray-400 transition"
        >
          🔄 Limpiar
        </button>
      </div>

      {/* Info */}
      <div className="mt-6 bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg text-sm">
        <p>
          <strong>ℹ️ Nota:</strong> Las respuestas se guardarán localmente. En
          futuras versiones se evaluarán automáticamente usando criterios PAU.
        </p>
      </div>
    </div>
  );
}