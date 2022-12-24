-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 24, 2022 at 09:22 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dev-kampungsiberdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `acc_consultation_req`
--

CREATE TABLE `acc_consultation_req` (
  `id` int(11) NOT NULL,
  `consultation_req_id` int(11) DEFAULT NULL,
  `link_zoom` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `acc_consultation_req`
--

INSERT INTO `acc_consultation_req` (`id`, `consultation_req_id`, `link_zoom`) VALUES
(1, 1, 'ini linknya'),
(2, 1, 'ini link zoom');

-- --------------------------------------------------------

--
-- Table structure for table `available_consult_time`
--

CREATE TABLE `available_consult_time` (
  `id` int(11) NOT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `available_consult_time`
--

INSERT INTO `available_consult_time` (`id`, `start_time`, `end_time`) VALUES
(1, '16:00:00', '18:00:00'),
(2, '10:00:00', '12:00:00'),
(3, '19:00:00', '21:00:00'),
(4, '08:00:00', '10:00:00'),
(5, '10:00:00', '11:00:00'),
(6, '13:00:00', '15:00:00'),
(7, '15:00:00', '17:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `consultation_request`
--

CREATE TABLE `consultation_request` (
  `id` int(11) NOT NULL,
  `requestor_id` int(11) DEFAULT NULL,
  `mentor_id` int(11) DEFAULT NULL,
  `consultation_date` date DEFAULT NULL,
  `is_accepted_mentor` int(11) DEFAULT NULL,
  `verify_payment` int(11) DEFAULT NULL,
  `avail_time_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `consultation_request`
--

INSERT INTO `consultation_request` (`id`, `requestor_id`, `mentor_id`, `consultation_date`, `is_accepted_mentor`, `verify_payment`, `avail_time_id`) VALUES
(5, 75, 74, '2022-12-25', NULL, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `mentor_avail_time`
--

CREATE TABLE `mentor_avail_time` (
  `id` int(11) NOT NULL,
  `mentor_id` int(11) DEFAULT NULL,
  `avail_time_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mentor_avail_time`
--

INSERT INTO `mentor_avail_time` (`id`, `mentor_id`, `avail_time_id`) VALUES
(1, 1, 1),
(2, 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `mentor_stack`
--

CREATE TABLE `mentor_stack` (
  `id` int(11) NOT NULL,
  `mentor_id` int(11) DEFAULT NULL,
  `tech_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mentor_stack`
--

INSERT INTO `mentor_stack` (`id`, `mentor_id`, `tech_id`) VALUES
(1, 74, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tech_stack`
--

CREATE TABLE `tech_stack` (
  `id` int(11) NOT NULL,
  `stack_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tech_stack`
--

INSERT INTO `tech_stack` (`id`, `stack_name`) VALUES
(1, 'Python'),
(2, 'React Js'),
(3, 'Kotlin'),
(4, 'Swift'),
(5, 'Vue Js'),
(6, 'Laravel');

-- --------------------------------------------------------

--
-- Table structure for table `testimonial_compro`
--

CREATE TABLE `testimonial_compro` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `testimonial_content` text DEFAULT NULL,
  `created_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `testimonial_compro`
--

INSERT INTO `testimonial_compro` (`id`, `user_id`, `testimonial_content`, `created_date`) VALUES
(1, 75, 'ad wfaewf fsd fsd fas fasd fasd', '2022-12-24'),
(2, 74, 'asndnasjkdnkjasndjk asndjkasnd naskj', '2022-12-23');

-- --------------------------------------------------------

--
-- Table structure for table `testimonial_mentor`
--

CREATE TABLE `testimonial_mentor` (
  `id` int(11) NOT NULL,
  `requestor_id` int(11) DEFAULT NULL,
  `mentor_id` int(11) DEFAULT NULL,
  `testimonial_content` text DEFAULT NULL,
  `created_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `testimonial_mentor`
--

INSERT INTO `testimonial_mentor` (`id`, `requestor_id`, `mentor_id`, `testimonial_content`, `created_date`) VALUES
(1, 74, 75, 'andasndj good', '2022-12-24'),
(2, 74, 75, 'maslkdmlkamdklas maskdmlaksmd', '2022-12-23');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `reg_type` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `email`, `password`, `reg_type`, `full_name`, `first_name`, `last_name`) VALUES
(74, 'aqmal.pratama88@gmail.com', 'pbkdf2:sha256:260000$b5yfoDw9FlNMxfLB$1ac1ec654e8ac821ea89129d0c53cb0e3345cdc82f230827ccbad1a083a2a765', 1, 'Muhammad Aqmal Khafidz Pratama', 'Muhammad Aqmal', 'Khafidz Pratama'),
(75, 'raflysurya@gmail.com', 'pbkdf2:sha256:260000$MyxzugJRZKvGfwrr$4d97a46d5b1db5094b15dfb4b01bf3b393e2207eb9cfed1ba485bba48de6d657', 2, 'Muhammad Rafly Surya Nirwana', 'Muhammad Rafly', 'Surya Nirwana'),
(78, 'aqmal.pratama81@gmail.com', 'pbkdf2:sha256:260000$KF3U26YH1HwCeWBb$82ce19f3c7d55bf8db47475df2b91a0222c775802600d7c34814ef15befb18b8', 1, 'Aqmal Pratama', 'Aqmal', 'Pratama');

-- --------------------------------------------------------

--
-- Table structure for table `user_profile`
--

CREATE TABLE `user_profile` (
  `id` int(11) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `university` varchar(255) DEFAULT NULL,
  `no_phone` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `photo_name` varchar(255) DEFAULT NULL,
  `reg_type` int(11) DEFAULT NULL,
  `is_approved_admin` int(11) DEFAULT NULL,
  `rate_per_hour` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_profile`
--

INSERT INTO `user_profile` (`id`, `full_name`, `email`, `first_name`, `last_name`, `birth_date`, `university`, `no_phone`, `user_id`, `photo_name`, `reg_type`, `is_approved_admin`, `rate_per_hour`) VALUES
(11, 'Muhammad Aqmal Khafidz Pratama', 'aqmal.pratama88@gmail.com', 'Muhammad Aqmal', 'Khafidz Pratama', '2002-04-02', 'unj', '0088771123', 74, '0922720a8b2592e397ff7a7ed19e2056.jpg', 1, 1, '80000'),
(12, 'Muhammad Rafly Surya Nirwana', 'raflysurya@gmail.com', 'Muhammad Rafly', 'Surya Nirwana', '2002-04-09', 'unj', '081234521723', 75, NULL, 2, NULL, NULL),
(15, 'Aqmal Pratama', 'aqmal.pratama81@gmail.com', 'Aqmal', 'Pratama', '2002-04-28', 'unj', '081234521723', 78, NULL, 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_consultation_request`
-- (See below for the actual view)
--
CREATE TABLE `vw_consultation_request` (
`id` int(11)
,`consultation_date` varchar(10)
,`req_name` varchar(255)
,`mentor_name` varchar(255)
,`avail_time_id` int(11)
,`start_time` varchar(8)
,`end_time` varchar(8)
,`mentor_id` int(11)
,`requestor_id` int(11)
,`is_accepted_mentor` int(11)
,`verify_payment` int(11)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_mentor_stack`
-- (See below for the actual view)
--
CREATE TABLE `vw_mentor_stack` (
`id` int(11)
,`mentor_id` int(11)
,`tech_id` int(11)
,`full_name` varchar(255)
,`stack_name` varchar(255)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_testimonial_compro`
-- (See below for the actual view)
--
CREATE TABLE `vw_testimonial_compro` (
`id` int(11)
,`user_id` int(11)
,`full_name` varchar(255)
,`testimonial_content` text
,`created_date` varchar(10)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_testimonial_mentor`
-- (See below for the actual view)
--
CREATE TABLE `vw_testimonial_mentor` (
`id` int(11)
,`requestor_id` int(11)
,`req_name` varchar(255)
,`mentor_id` int(11)
,`mentor_name` varchar(255)
,`testimonial_content` text
,`created_date` varchar(10)
);

-- --------------------------------------------------------

--
-- Structure for view `vw_consultation_request`
--
DROP TABLE IF EXISTS `vw_consultation_request`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_consultation_request`  AS SELECT `cr`.`id` AS `id`, date_format(`cr`.`consultation_date`,'%Y-%m-%d') AS `consultation_date`, `requestor`.`full_name` AS `req_name`, `mentor`.`full_name` AS `mentor_name`, `cr`.`avail_time_id` AS `avail_time_id`, date_format(`act`.`start_time`,'%T') AS `start_time`, date_format(`act`.`end_time`,'%T') AS `end_time`, `mentor`.`id` AS `mentor_id`, `requestor`.`id` AS `requestor_id`, `cr`.`is_accepted_mentor` AS `is_accepted_mentor`, `cr`.`verify_payment` AS `verify_payment` FROM (((`consultation_request` `cr` left join `user` `requestor` on(`requestor`.`id` = `cr`.`requestor_id`)) left join `user` `mentor` on(`mentor`.`id` = `cr`.`mentor_id`)) left join `available_consult_time` `act` on(`act`.`id` = `cr`.`avail_time_id`))  ;

-- --------------------------------------------------------

--
-- Structure for view `vw_mentor_stack`
--
DROP TABLE IF EXISTS `vw_mentor_stack`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_mentor_stack`  AS SELECT `ms`.`id` AS `id`, `ms`.`mentor_id` AS `mentor_id`, `ms`.`tech_id` AS `tech_id`, `u`.`full_name` AS `full_name`, `ts`.`stack_name` AS `stack_name` FROM ((`mentor_stack` `ms` left join `user` `u` on(`u`.`id` = `ms`.`mentor_id`)) left join `tech_stack` `ts` on(`ts`.`id` = `ms`.`tech_id`))  ;

-- --------------------------------------------------------

--
-- Structure for view `vw_testimonial_compro`
--
DROP TABLE IF EXISTS `vw_testimonial_compro`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_testimonial_compro`  AS SELECT `tc`.`id` AS `id`, `tc`.`user_id` AS `user_id`, `u`.`full_name` AS `full_name`, `tc`.`testimonial_content` AS `testimonial_content`, date_format(`tc`.`created_date`,'%Y-%m-%d') AS `created_date` FROM (`testimonial_compro` `tc` left join `user` `u` on(`u`.`id` = `tc`.`user_id`))  ;

-- --------------------------------------------------------

--
-- Structure for view `vw_testimonial_mentor`
--
DROP TABLE IF EXISTS `vw_testimonial_mentor`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_testimonial_mentor`  AS SELECT `tm`.`id` AS `id`, `tm`.`requestor_id` AS `requestor_id`, `u`.`full_name` AS `req_name`, `tm`.`mentor_id` AS `mentor_id`, `m`.`full_name` AS `mentor_name`, `tm`.`testimonial_content` AS `testimonial_content`, date_format(`tm`.`created_date`,'%Y-%m-%d') AS `created_date` FROM ((`testimonial_mentor` `tm` left join `user` `u` on(`u`.`id` = `tm`.`requestor_id`)) left join `user` `m` on(`m`.`id` = `tm`.`mentor_id`))  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `acc_consultation_req`
--
ALTER TABLE `acc_consultation_req`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `available_consult_time`
--
ALTER TABLE `available_consult_time`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `consultation_request`
--
ALTER TABLE `consultation_request`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mentor_avail_time`
--
ALTER TABLE `mentor_avail_time`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mentor_stack`
--
ALTER TABLE `mentor_stack`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tech_stack`
--
ALTER TABLE `tech_stack`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `testimonial_compro`
--
ALTER TABLE `testimonial_compro`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `testimonial_mentor`
--
ALTER TABLE `testimonial_mentor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `acc_consultation_req`
--
ALTER TABLE `acc_consultation_req`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `available_consult_time`
--
ALTER TABLE `available_consult_time`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `consultation_request`
--
ALTER TABLE `consultation_request`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `mentor_avail_time`
--
ALTER TABLE `mentor_avail_time`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `mentor_stack`
--
ALTER TABLE `mentor_stack`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tech_stack`
--
ALTER TABLE `tech_stack`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `testimonial_compro`
--
ALTER TABLE `testimonial_compro`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `testimonial_mentor`
--
ALTER TABLE `testimonial_mentor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `user_profile`
--
ALTER TABLE `user_profile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
