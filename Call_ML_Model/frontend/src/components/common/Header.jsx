import { useEffect, useState } from 'react';
import { checkHealth } from '../../services/agentService';

const Header = () => {
  const [isHealthy, setIsHealthy] = useState(true);

  useEffect(() => {
    const verifyHealth = async () => {
      try {
        await checkHealth();
        setIsHealthy(true);
      } catch (e) {
        setIsHealthy(false);
      }
    };
    verifyHealth();
  }, []);

  return (
   <>
      <header>
        <div className="container mx-auto px-2 py-4 flex justify-between max-w-6xl">
          <div className="flex items-center gap-2">
            <div>
              <h1 className="text-lg text-gray items-center">Predictor</h1>
              <p className="text-xs text-gray-400 font-medium tracking-wide">Iris Titanic Loan</p>
              
            </div>
          </div>
        </div>
      </header>
   </>
  );
};

export default Header;
