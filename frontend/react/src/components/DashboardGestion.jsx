import React, { useState, useEffect } from 'react';
import { Users, TrendingUp, Award, Clock } from 'lucide-react';
import MetricCard from './MetricCard';
import Charts from './Charts';
import { getDashboardGestion } from '../services/api';

const DashboardGestion = ({ selectedMonth }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await getDashboardGestion(selectedMonth);
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
  }, [selectedMonth]);

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
  const total = metricas.total_triajes || 0;
  const pctCriticos = total > 0 ? ((metricas.criticos || 0) / total * 100).toFixed(1) : 0;
  const pctAltos = total > 0 ? ((metricas.altos || 0) / total * 100).toFixed(1) : 0;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard
          title="Total del Mes"
          value={metricas.total_triajes || 0}
          subtitle={selectedMonth}
          icon={Users}
        />
        <MetricCard
          title="Críticos"
          value={metricas.criticos || 0}
          subtitle={`${pctCriticos}% del total`}
          icon={TrendingUp}
          variant="danger"
        />
        <MetricCard
          title="Altos"
          value={metricas.altos || 0}
          subtitle={`${pctAltos}% del total`}
          icon={TrendingUp}
          variant="warning"
        />
        <MetricCard
          title="Moderados"
          value={metricas.moderados || 0}
          icon={TrendingUp}
        />
        <MetricCard
          title="Bajos"
          value={metricas.bajos || 0}
          icon={TrendingUp}
          variant="success"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Charts
          type="line"
          title="Triajes por Día"
          data={(data?.triajes_por_dia || []).map(item => ({
            fecha: new Date(item.fecha).toLocaleDateString('es-CO', { day: 'numeric', month: 'short' }),
            cantidad: item.cantidad
          }))}
        />
        <Charts
          type="horizontal-bar"
          title="Triajes por Profesional"
          data={data?.triajes_por_profesional || []}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Charts
          type="pie"
          title="Distribución por Nivel de Urgencia"
          data={data?.distribucion_urgencia || []}
        />
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-700 mb-4">Análisis de Tendencias</h3>
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg">
              <p className="text-sm text-slate-500">Casos Críticos</p>
              <p className="text-2xl font-bold text-danger-600">{pctCriticos}%</p>
              {pctCriticos > 10 && (
                <p className="text-sm text-warning-600 mt-1">Porcentaje elevado - revisar procesos</p>
              )}
            </div>
            <div className="p-4 bg-slate-50 rounded-lg">
              <p className="text-sm text-slate-500">Casos de Alta Prioridad</p>
              <p className="text-2xl font-bold text-warning-600">{pctAltos}%</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg">
              <p className="text-sm text-slate-500">Promedio de Tiempo</p>
              <p className="text-2xl font-bold text-slate-700">
                {typeof metricas.tiempo_promedio_minutos === 'number' ? `${metricas.tiempo_promedio_minutos.toFixed(1)} min` : 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardGestion;
