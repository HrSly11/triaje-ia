import React, { useState, useEffect } from 'react';
import { Users, Clock, AlertTriangle, Activity } from 'lucide-react';
import MetricCard from './MetricCard';
import Charts from './Charts';
import { getDashboardOperacional } from '../services/api';

const DashboardOperativo = ({ selectedDate }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await getDashboardOperacional(selectedDate);
        setData(result);
        setError(null);
      } catch (err) {
        setError('Error al cargar datos del dashboard');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedDate]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64 bg-danger-50 rounded-lg">
        <p className="text-danger-600">{error}</p>
      </div>
    );
  }

  const metricas = data?.metricas || {};

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Triajes"
          value={metricas.total_triajes || 0}
          subtitle="Hoy"
          icon={Users}
        />
        <MetricCard
          title="Casos Críticos"
          value={metricas.criticos || 0}
          subtitle="Requieren atención inmediata"
          icon={AlertTriangle}
          variant="danger"
          trend={metricas.criticos > 0 ? 'up' : 'neutral'}
          trendValue={metricas.criticos > 0 ? 'Atención requerida' : 'Sin casos críticos'}
        />
        <MetricCard
          title="Casos Altos"
          value={metricas.altos || 0}
          subtitle="Prioridad alta"
          icon={AlertTriangle}
          variant="warning"
        />
        <MetricCard
          title="Tiempo Promedio"
          value={metricas.tiempo_promedio_minutos != null ? `${parseFloat(metricas.tiempo_promedio_minutos).toFixed(1)} min` : 'N/A'}
          subtitle="Duración promedio de atención"
          icon={Clock}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Charts
          type="pie"
          title="Distribución por Nivel de Urgencia"
          data={data?.distribucion_urgencia || []}
        />
        <Charts
          type="bar"
          title="Triajes por Hora"
          data={(data?.triajes_por_hora || []).map(item => ({
            nombre: new Date(item.hora).toLocaleTimeString('es-CO', { hour: '2-digit' }),
            cantidad: item.cantidad
          }))}
        />
      </div>
    </div>
  );
};

export default DashboardOperativo;
