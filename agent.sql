-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: db_agent
-- Tiempo de generación: 01-08-2025 a las 02:49:11
-- Versión del servidor: 8.0.40
-- Versión de PHP: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `agent`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id` int NOT NULL,
  `categoria` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `categoria`) VALUES
(1, 'Emprendedores');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `links`
--

CREATE TABLE `links` (
  `id` int NOT NULL,
  `medio` varchar(255) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `link` varchar(255) NOT NULL,
  `fecha` datetime NOT NULL,
  `nota` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `links`
--

INSERT INTO `links` (`id`, `medio`, `titulo`, `link`, `fecha`, `nota`) VALUES
(65, 'FORBES PY', 'Firmas paraguayas podrán medirse ante las regionales y analizar su competitividad, con encuesta de \"Maduración Empresarial\"', 'https://www.forbes.com.py/negocios/firmas-paraguayas-podran-medirse-regionales-analizar-su-competitividad-encuesta-maduracion-empresarial-n76054', '2025-07-31 21:45:19', 'No'),
(66, 'FORBES PY', 'De ganar un Oscar a emprender en salud: Halle Berry apuesta todo por una startup para mujeres mayores de 50 años', 'https://www.forbes.com.py/millonarios/de-ganar-oscar-emprender-salud-halle-berry-apuesta-todo-una-startup-mujeres-mayores-50-anos-n76079', '2025-07-31 21:45:19', 'No'),
(69, 'ABC', 'Lanzan programa para impulsar exportación vía e-commerce: ¿de qué trata?', 'https://www.abc.com.py/economia/2025/07/31/lanzan-programa-para-impulsar-exportacion-via-e-commerce-de-que-trata/#comments-section', '2025-07-31 21:45:58', 'No'),
(70, 'ULTIMA HORA', 'Proponen talleres gratuitos para potenciar a las mipymes', 'https://www.ultimahora.com/proponen-talleres-gratuitos-para-potenciar-a-las-mipymes', '2025-07-31 21:46:08', 'No');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notas`
--

CREATE TABLE `notas` (
  `id` int NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `id_categoria` int NOT NULL,
  `ultima_modificacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `links`
--
ALTER TABLE `links`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `notas`
--
ALTER TABLE `notas`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `links`
--
ALTER TABLE `links`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT de la tabla `notas`
--
ALTER TABLE `notas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
