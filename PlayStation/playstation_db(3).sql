-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2025 at 08:59 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `playstation_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `cache`
--

CREATE TABLE `cache` (
  `key` varchar(255) NOT NULL,
  `value` mediumtext NOT NULL,
  `expiration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cache_locks`
--

CREATE TABLE `cache_locks` (
  `key` varchar(255) NOT NULL,
  `owner` varchar(255) NOT NULL,
  `expiration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `uuid` varchar(255) NOT NULL,
  `connection` text NOT NULL,
  `queue` text NOT NULL,
  `payload` longtext NOT NULL,
  `exception` longtext NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `queue` varchar(255) NOT NULL,
  `payload` longtext NOT NULL,
  `attempts` tinyint(3) UNSIGNED NOT NULL,
  `reserved_at` int(10) UNSIGNED DEFAULT NULL,
  `available_at` int(10) UNSIGNED NOT NULL,
  `created_at` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `job_batches`
--

CREATE TABLE `job_batches` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `total_jobs` int(11) NOT NULL,
  `pending_jobs` int(11) NOT NULL,
  `failed_jobs` int(11) NOT NULL,
  `failed_job_ids` longtext NOT NULL,
  `options` mediumtext DEFAULT NULL,
  `cancelled_at` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  `finished_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '0001_01_01_000000_create_users_table', 1),
(2, '0001_01_01_000001_create_cache_table', 1),
(3, '0001_01_01_000002_create_jobs_table', 1),
(4, '2025_06_11_052740_create_sessions_table', 2);

-- --------------------------------------------------------

--
-- Table structure for table `mps`
--

CREATE TABLE `mps` (
  `id` int(11) NOT NULL,
  `product_metric_id` int(11) NOT NULL,
  `month` varchar(10) NOT NULL,
  `demand` int(11) NOT NULL,
  `production` int(11) NOT NULL,
  `subcontract` int(11) NOT NULL DEFAULT 0,
  `cost` decimal(12,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mps`
--

INSERT INTO `mps` (`id`, `product_metric_id`, `month`, `demand`, `production`, `subcontract`, `cost`, `created_at`, `updated_at`) VALUES
(1, 1, 'Jun', 1200, 1000, 200, 420000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(2, 1, 'Jul', 1300, 1100, 200, 455000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(3, 1, 'Ago', 1250, 1250, 0, 525000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(4, 2, 'Jun', 900, 850, 50, 320000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(5, 2, 'Jul', 950, 900, 50, 340000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(6, 2, 'Ago', 920, 920, 0, 345000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(7, 3, 'Jun', 600, 500, 100, 105000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(8, 3, 'Jul', 650, 550, 100, 110000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(9, 3, 'Ago', 620, 620, 0, 115000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(10, 4, 'Jun', 800, 800, 0, 96000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(11, 4, 'Jul', 850, 800, 50, 98000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29'),
(12, 4, 'Ago', 870, 870, 0, 100000.00, '2025-06-11 17:12:29', '2025-06-11 17:12:29');

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `production_plans`
--

CREATE TABLE `production_plans` (
  `id` int(11) NOT NULL,
  `alternative_name` varchar(100) NOT NULL,
  `total_cost` decimal(12,2) NOT NULL COMMENT 'Costo total en bolivianos',
  `advantages` text NOT NULL,
  `disadvantages` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `production_plans`
--

INSERT INTO `production_plans` (`id`, `alternative_name`, `total_cost`, `advantages`, `disadvantages`, `created_at`, `updated_at`) VALUES
(1, 'Inventario Cero', 49500.00, 'Sin exceso de stock', 'Costos altos por contrataciones/despidos', '2025-06-11 08:09:27', '2025-06-11 08:09:27'),
(2, 'Fuerza de Trabajo Constante', 50000.00, 'Estabilidad laboral', 'Costos de almacenamiento', '2025-06-11 08:09:27', '2025-06-11 08:09:27'),
(3, 'Subcontratación Parcial', 46000.00, 'Flexibilidad y bajo costo', 'Dependencia de terceros', '2025-06-11 08:09:27', '2025-06-11 08:09:27'),
(4, 'Contratar/Despedir', 51500.00, 'Adaptación rápida', 'Inestabilidad laboral', '2025-06-11 08:09:27', '2025-06-11 08:09:27'),
(5, 'Constancia + Horas Extra', 48000.00, 'Equilibrio entre costos y flexibilidad', 'Costos de horas extra', '2025-06-11 08:09:27', '2025-06-11 08:09:27');

-- --------------------------------------------------------

--
-- Table structure for table `production_problems`
--

CREATE TABLE `production_problems` (
  `id` int(11) NOT NULL,
  `problem_name` varchar(100) NOT NULL,
  `frequency` int(11) NOT NULL COMMENT 'Casos mensuales',
  `percentage` decimal(5,2) NOT NULL COMMENT 'Porcentaje sobre total',
  `cumulative_percentage` decimal(5,2) NOT NULL COMMENT 'Porcentaje acumulado',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `production_problems`
--

INSERT INTO `production_problems` (`id`, `problem_name`, `frequency`, `percentage`, `cumulative_percentage`, `created_at`, `updated_at`) VALUES
(1, 'Fallos de ensamblaje', 60, 36.86, 36.84, '2025-06-11 08:08:29', '2025-06-11 23:17:27'),
(2, 'Errores de firmware', 50, 26.32, 63.16, '2025-06-11 08:08:29', '2025-06-12 08:36:01'),
(3, 'Problemas de stock', 40, 21.05, 84.21, '2025-06-11 08:08:29', '2025-06-11 08:08:29'),
(4, 'Retrasos logísticos', 20, 10.53, 94.74, '2025-06-11 08:08:29', '2025-06-11 08:08:29'),
(5, 'Baja calidad en controles', 10, 5.26, 100.00, '2025-06-11 08:08:29', '2025-06-11 08:08:29');

-- --------------------------------------------------------

--
-- Table structure for table `product_metrics`
--

CREATE TABLE `product_metrics` (
  `id` int(11) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `income` decimal(12,2) NOT NULL COMMENT 'Ingresos en dólares',
  `total_costs` decimal(12,2) NOT NULL COMMENT 'Costos totales en dólares',
  `profit` decimal(12,2) NOT NULL COMMENT 'Utilidad en dólares',
  `profitability` decimal(5,2) NOT NULL COMMENT 'Rentabilidad porcentual',
  `marketability` decimal(5,2) NOT NULL COMMENT 'Comerciabilidad porcentual',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_metrics`
--

INSERT INTO `product_metrics` (`id`, `product_name`, `income`, `total_costs`, `profit`, `profitability`, `marketability`, `created_at`, `updated_at`) VALUES
(1, 'PS5 Standard', 500.00, 420.00, 130.00, 47.50, 49.38, '2025-06-11 08:07:13', '2025-06-11 23:54:36'),
(2, 'PS5 Digital', 500.00, 370.00, 80.00, 26.00, 30.86, '2025-06-11 08:07:13', '2025-06-11 23:54:36'),
(3, 'DualSense Edge', 200.00, 150.00, 50.00, 25.00, 12.35, '2025-06-11 08:07:13', '2025-06-11 23:54:36'),
(4, 'PS Plus Suscripción', 120.00, 40.00, 80.00, 66.67, 7.41, '2025-06-11 08:07:13', '2025-06-11 23:54:36');

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `payload` longtext NOT NULL,
  `last_activity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','normal') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'admin', '$2y$12$RgKqXdgenJsOrHQyjQ1hW.FhXWZUCDzaLUFVufdB602GgJGG4Gwvy', 'admin', '2025-06-10 21:54:00'),
(2, 'user1', '$2y$10$X8Y7Z6X5Y4Z3X2Y1W9X8Y..Z7Y5X3Z2W1Y9X8Z7Y6X5Z4Y3W2X', 'normal', '2025-06-10 21:54:00'),
(3, 'dario', '$2y$10$U1vuU8q9Gpq/EK4UUKSReew1oJ97gRQ4C62MXxwuvb13mNiNVuO4m', 'admin', '2025-06-10 22:06:15'),
(4, 'admin2', '$2y$12$AHLPDY6naAqF2pZOwJRCl.ZQ0QuFjsSZFb/qnrNjnQWvYWdgD7H.K', 'admin', '2025-06-11 06:23:01'),
(5, 'empleado2', '$2y$12$yhnLx1SfpIyUQoRxT71Sn.BjVAG.4PL1RrZifMJJt7PRJZdM5065W', 'normal', '2025-06-11 06:23:01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cache`
--
ALTER TABLE `cache`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `cache_locks`
--
ALTER TABLE `cache_locks`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobs_queue_index` (`queue`);

--
-- Indexes for table `job_batches`
--
ALTER TABLE `job_batches`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mps`
--
ALTER TABLE `mps`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_metric_id` (`product_metric_id`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `production_plans`
--
ALTER TABLE `production_plans`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `production_problems`
--
ALTER TABLE `production_problems`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_metrics`
--
ALTER TABLE `product_metrics`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessions_user_id_index` (`user_id`),
  ADD KEY `sessions_last_activity_index` (`last_activity`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `mps`
--
ALTER TABLE `mps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `production_plans`
--
ALTER TABLE `production_plans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `production_problems`
--
ALTER TABLE `production_problems`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `product_metrics`
--
ALTER TABLE `product_metrics`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `mps`
--
ALTER TABLE `mps`
  ADD CONSTRAINT `mps_ibfk_1` FOREIGN KEY (`product_metric_id`) REFERENCES `product_metrics` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
