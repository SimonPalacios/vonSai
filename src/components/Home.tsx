import React from 'react';

const Home: React.FC = () => {
  return (
    <article className="grid place-items-center bg-gray-200">
      <section className="bg-white shadow-md rounded-lg p-6 w-1/2 h-1/2">
        <h1 className="text-2xl font-bold mb-4 border-b border-amber-700">Sp</h1>
        <p className="text-gray-700">
          Hola! El proposito de ésta página es jugar un poco con el diseño y la estructura de una página web. De pasada buscar una forma de juntar los repositorios de compañeros de la facultad que utilizo como apoyo en la carrera. 
        </p>
      </section>
    </article>
  );
};

export default Home;