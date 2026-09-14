import { useState, useCallback } from 'react';
import { analyzeIris } from '../services/agentService';

export function useBotanicalAgent() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [domain, setDomain] = useState(null);
  const [processingTime, setProcessingTime] = useState(0);

  const analyze = useCallback(async (query) => {
    setLoading(true);
    setError(null);
    try {
      const response = await analyzeIris(query);
      if (response.success) {
        setResult(response.data);
        setDomain(response.data?.domain || null);
        setProcessingTime(response.processing_time_ms || 0);
      } else {
        setError(response.error || 'Unknown error');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResult(null);
    setDomain(null);
    setError(null);
    setProcessingTime(0);
  }, []);

  return { loading, error, result, domain, processingTime, analyze, reset };
}
