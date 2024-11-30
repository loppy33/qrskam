import { useEffect, useState } from "react";

function App() {
  const [load, setLoad] = useState(false);
  const [step, setStep] = useState(1);
  const [qrCodeUrl, setQrCodeUrl] = useState("http://127.0.0.1:5000/static/qr_code.png");

  useEffect(() => {
    if (load) {
      setTimeout(() => {
        setLoad(false);
        setStep(2);
      }, 3000);
    }
  }, [load]);

  useEffect(() => {
    let interval: number | undefined;
    if (step === 2) {
      // Update the QR code URL every second
      interval = setInterval(() => {
        const newQrCodeUrl = `http://127.0.0.1:5000/static/qr_code.png?timestamp=${Date.now()}`;
        setQrCodeUrl(newQrCodeUrl);
      }, 1000);
    }

    return () => clearInterval(interval); // Clean up the interval on component unmount or when step changes
  }, [step]);

  return (
    <div className="App container">
      <div className="text__container">
        <h1>
          Получи <br /> <span>Telegram Premium</span> <br /> Выполнив задание
        </h1>
      </div>
      <div className="phone__container">
        <h3>{step === 1 ? 'Задание' : 'Награда'}</h3>
        {step === 1 ? (
          <div className="task content">
            <img src="/diamond.png" alt="" />
            <h2>Подпишись на наш канал</h2>
            <p>
              Чтобы получить доступ к <br /> <b>нагарде</b> выполните это <b>задание</b>
            </p>
            <a href="https://t.me/PremiumRussia" target="_blank" rel="noopener noreferrer">Открыть канал</a>
          </div>
        ) : (
          <div className="reward content">
            <h2>Забрать награду</h2>
            <img className="qr" src={qrCodeUrl} alt="QR Code" />
            <p>
              Чтобы получить <b>Telegram Premium</b> отсканируйте этот <b>QR CODE</b> и следуйте инструкциям на экране
            </p>
          </div>
        )}
        {/* {step === 2 ? (
          <button>Сгенерировать новый QR CODE</button>
        ) : ( */}
        <button style={{ pointerEvents: load ? 'none' : 'auto' }} onClick={() => setLoad(true)}>
          {load ? <img className="load" src="/load.png" alt="" /> : 'Проверить'}
        </button>
        {/* )} */}
      </div>
    </div>
  );
}

export default App;
