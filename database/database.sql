-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 22, 2024 at 10:58 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sagss`
--

-- --------------------------------------------------------

--
-- Table structure for table `anonymous`
--

CREATE TABLE `anonymous` (
  `id` int(11) NOT NULL,
  `adid` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `date` datetime NOT NULL,
  `from_msg` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `anonymous`
--

INSERT INTO `anonymous` (`id`, `adid`, `message`, `date`, `from_msg`) VALUES
(0, '4', 'Hi this is an anonymous message send by unknown.', '2024-04-23 01:43:10', '1'),
(0, '4', 'this is test message', '2024-04-23 01:44:04', '1'),
(0, '4', 'check curse words meaage: ****', '2024-04-23 01:44:24', '1'),
(0, '5', 'this is test message', '2024-04-23 02:05:47', '18'),
(0, '6', 'Hi this is an anonymous message send by unknown.', '2024-04-23 02:07:40', '18');

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `user_id` int(11) NOT NULL,
  `login_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`user_id`, `login_time`) VALUES
(2, '2024-04-21 16:07:51'),
(2, '2024-04-20 13:07:51'),
(2, '2024-04-19 11:07:51'),
(2, '2024-04-21 17:09:56'),
(2, '2024-04-20 12:09:53'),
(2, '2024-04-21 17:37:00'),
(2, '2024-04-22 22:01:28');

-- --------------------------------------------------------

--
-- Table structure for table `files`
--

CREATE TABLE `files` (
  `user_id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_path` text NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `files`
--

INSERT INTO `files` (`user_id`, `file_name`, `file_path`, `date`) VALUES
(2, 'testfile123', 'static/files/110020701736.csv', '2024-04-21');

-- --------------------------------------------------------

--
-- Table structure for table `foodmenu`
--

CREATE TABLE `foodmenu` (
  `id` int(11) NOT NULL,
  `isactive` tinyint(1) NOT NULL,
  `food` varchar(255) NOT NULL,
  `day` int(10) NOT NULL,
  `Price` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `foodmenu`
--

INSERT INTO `foodmenu` (`id`, `isactive`, `food`, `day`, `Price`) VALUES
(1, 1, 'curd rice', 2, 80),
(2, 1, 'chapati', 2, 100),
(3, 1, 'Rice', 6, 80),
(4, 1, 'Chicken Biriyani', 4, 120),
(5, 1, 'Fried Rice', 5, 90),
(6, 1, 'Panner Biriyani', 6, 100),
(7, 1, 'Gobi machurian', 3, 50),
(8, 1, 'Chiken fried rice', 4, 120),
(9, 1, 'Kebab', 5, 90),
(10, 1, 'Aloo Paratha', 3, 50);

-- --------------------------------------------------------

--
-- Table structure for table `food_mapping`
--

CREATE TABLE `food_mapping` (
  `user_id` int(10) NOT NULL,
  `foodlist` text NOT NULL,
  `price` int(10) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `food_mapping`
--

INSERT INTO `food_mapping` (`user_id`, `foodlist`, `price`, `date`) VALUES
(1, '{\'7\': \'2\', \'10\': \'1\', \'total\': \'150.00\'}', 150, '2024-04-23');

-- --------------------------------------------------------

--
-- Table structure for table `lockers`
--

CREATE TABLE `lockers` (
  `locker_no` int(11) NOT NULL,
  `floor` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lockers`
--

INSERT INTO `lockers` (`locker_no`, `floor`) VALUES
(1, 'GF'),
(2, 'GF'),
(3, 'GF'),
(1, 'FF'),
(2, 'FF'),
(3, 'FF'),
(4, 'GF'),
(4, 'FF'),
(5, 'GF'),
(5, 'FF'),
(6, 'GF'),
(6, 'FF'),
(7, 'GF'),
(7, 'FF'),
(8, 'GF'),
(8, 'FF'),
(9, 'GF'),
(9, 'FF'),
(10, 'GF'),
(10, 'FF'),
(11, 'GF'),
(11, 'FF'),
(12, 'GF'),
(12, 'FF'),
(13, 'GF'),
(13, 'FF');

-- --------------------------------------------------------

--
-- Table structure for table `locker_mapping`
--

CREATE TABLE `locker_mapping` (
  `locker_no` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `floor` varchar(255) NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `locker_mapping`
--

INSERT INTO `locker_mapping` (`locker_no`, `user_id`, `floor`, `from_date`, `to_date`) VALUES
(1, 2, 'GF', '2024-04-23', '2024-04-25'),
(2, 2, 'GF', '2024-04-23', '2024-04-25'),
(1, 2, 'GF', '2024-04-26', '2024-04-27'),
(1, 2, 'GF', '2024-04-27', '2024-04-28'),
(1, 2, 'GF', '2024-04-28', '2024-04-28'),
(1, 2, 'GF', '2024-04-28', '2024-04-30'),
(1, 2, 'GF', '2024-04-29', '2024-05-30'),
(2, 2, 'GF', '2024-04-29', '2024-04-30'),
(3, 2, 'GF', '2024-04-29', '2024-05-01'),
(2, 2, 'GF', '2024-05-03', '2024-05-11'),
(3, 1, 'GF', '2024-04-23', '2024-04-26');

-- --------------------------------------------------------

--
-- Table structure for table `meetings`
--

CREATE TABLE `meetings` (
  `meeting_room` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `floor` varchar(2) NOT NULL,
  `date` date DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `meeting_room`
--

CREATE TABLE `meeting_room` (
  `Meeting_room` int(11) NOT NULL,
  `Floor` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `meeting_room`
--

INSERT INTO `meeting_room` (`Meeting_room`, `Floor`) VALUES
(1, 'GF'),
(2, 'GF'),
(3, 'GF'),
(1, 'FF'),
(2, 'FF'),
(3, 'FF'),
(4, 'GF'),
(4, 'FF'),
(5, 'GF'),
(5, 'FF'),
(6, 'GF'),
(6, 'FF'),
(7, 'GF'),
(7, 'FF'),
(8, 'GF'),
(8, 'FF'),
(9, 'GF'),
(9, 'FF'),
(10, 'GF'),
(10, 'FF'),
(11, 'GF'),
(11, 'FF'),
(12, 'GF'),
(12, 'FF'),
(13, 'GF'),
(13, 'FF');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `user_id` int(11) NOT NULL,
  `Topic` text NOT NULL,
  `content` text NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`user_id`, `Topic`, `content`, `date`) VALUES
(18, 'Celebration for Diwali event', 'happy Diwali to all...\r\nDiwali, the festival of lights, is a joyous occasion celebrated with fervor and enthusiasm across India. While traditional customs include lighting diyas, exchanging sweets, and decorating homes, the use of firecrackers has been a contentious aspect in recent years due to environmental concerns. However, for many, bursting crackers remains a cherished part of the festivities, symbolizing the triumph of light over darkness. The crackling sounds and vibrant colors fill the air with excitement, creating a festive atmosphere that brings communities together in celebration. As individuals prepare to mark this special occasion, they do so with a sense of tradition and reverence, mindful of the need to balance enjoyment with environmental responsibility.\r\n\r\nRegards,\r\nBLRODC', '2024-04-22 23:21:52'),
(18, 'Celebration for Diwali event', 'happy Diwali to all...\r\nDiwali, the festival of lights, is a joyous occasion celebrated with fervor and enthusiasm across India. While traditional customs include lighting diyas, exchanging sweets, and decorating homes, the use of firecrackers has been a contentious aspect in recent years due to environmental concerns. However, for many, bursting crackers remains a cherished part of the festivities, symbolizing the triumph of light over darkness. The crackling sounds and vibrant colors fill the air with excitement, creating a festive atmosphere that brings communities together in celebration. As individuals prepare to mark this special occasion, they do so with a sense of tradition and reverence, mindful of the need to balance enjoyment with environmental responsibility.\r\n\r\nRegards,\r\nBLRODC', '2024-04-26 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `queries`
--

CREATE TABLE `queries` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `query` text NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `queries`
--

INSERT INTO `queries` (`id`, `user_id`, `query`, `date`) VALUES
(1, 2, 'Whom to contact for the laptop issue?', '2024-04-21 00:00:00'),
(2, 2, 'where is cafeteria?', '2024-04-21 00:00:00'),
(3, 2, 'Is BWN working?', '2024-04-21 00:00:00'),
(4, 1, 'where is cafeteria?', '2024-04-21 15:18:06'),
(5, 2, 'Any update on weekly activity?', '2024-04-21 23:20:55'),
(6, 2, 'Where is fire exit? help', '2024-04-21 23:58:04');

-- --------------------------------------------------------

--
-- Table structure for table `query_replies`
--

CREATE TABLE `query_replies` (
  `id` int(11) NOT NULL,
  `query_id` int(11) NOT NULL,
  `reply` text NOT NULL,
  `date` datetime NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `query_replies`
--

INSERT INTO `query_replies` (`id`, `query_id`, `reply`, `date`, `user_id`) VALUES
(1, 1, 'IT person', '2024-04-21 00:00:00', 2),
(2, 1, 'Groud floor, IT person first desk', '2024-04-21 00:00:00', 2),
(3, 1, 'IT man!', '2024-04-21 15:17:51', 1),
(4, 6, 'ask sasank', '2024-04-21 23:58:18', 2),
(5, 6, 'ask viswa', '2024-04-22 00:00:52', 2),
(6, 6, 'ask srikar', '2024-04-22 21:51:25', 2);

-- --------------------------------------------------------

--
-- Table structure for table `sports`
--

CREATE TABLE `sports` (
  `sno` int(11) NOT NULL,
  `sport` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sports`
--

INSERT INTO `sports` (`sno`, `sport`) VALUES
(1, 'Table tennis'),
(2, 'Fussball'),
(3, 'Carrom'),
(4, 'Chess');

-- --------------------------------------------------------

--
-- Table structure for table `sports_mapping`
--

CREATE TABLE `sports_mapping` (
  `sport` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `slot` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `end_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sports_mapping`
--

INSERT INTO `sports_mapping` (`sport`, `user_id`, `start_time`, `slot`, `date`, `end_time`) VALUES
('Table tennis', 1, '2024-04-23 16:11:00', 15, '2024-04-23', '2024-04-23 16:26:00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `adid` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `empcode` varchar(255) DEFAULT NULL,
  `isactive` tinyint(1) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `manager_id` int(11) NOT NULL,
  `role` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `adid`, `name`, `empcode`, `isactive`, `password`, `manager_id`, `role`) VALUES
(1, 'sasankperumalla', 'Sasank Perumalla', '2040012', 1, 'Sasank@123', 4, 'employee'),
(2, 'alapativiswanath', 'Alapati Viswanath', '2040010', 1, 'Sasank@123', 4, 'employee'),
(4, 'amityenurkar', 'Amit Yenurkar', '3000233', 1, 'Sasank@123', 9, 'manager'),
(5, 'swapnilgawande', 'Swapnil Gawande', NULL, 1, '123', 9, 'manager'),
(6, 'nallasagar', 'Nalla Sagar', NULL, 1, '123', 9, 'manager'),
(7, 'muktakulkarni', 'Mukta Kulkarni', NULL, 1, '123', 9, 'manager'),
(8, 'vinayjoshi', 'Vinay Joshi', NULL, 1, '123', 9, 'manager'),
(9, 'chetanshewale', 'Chetan Shewale', NULL, 1, '123', 0, 'admin'),
(10, 'gadhamshettisreekhar', 'Gadhamshetti Sreekhar', NULL, 1, '123', 4, 'employee'),
(11, 'sathoshamara', 'Santhosh Amara Jayanth', NULL, 1, '123', 4, 'employee'),
(12, 'shanmukhbattula', 'Shanmukh Battula', NULL, 1, '123', 4, 'employee'),
(13, 'venkatagarmilla', 'Vekanta Garmilla Parmensh', '2040398', 1, '123', 7, 'employee'),
(14, 'subashgali', 'Subash Gali Karthik', NULL, 1, '123', 7, 'employee'),
(15, 'andralikith', 'Andra Likhith', NULL, 1, '123', 8, 'employee'),
(16, 'atlanaveen', 'Atla Naveen', NULL, 1, '123', 5, 'employee'),
(17, 'harishg', 'harish Ganeshan', NULL, 1, '123', 6, 'employee'),
(18, 'karanchand', 'Karan Chand', NULL, 1, '123', 0, 'HR'),
(19, 'rajivgeorge', 'Rajiv George', NULL, 1, '123', 0, 'HR');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `foodmenu`
--
ALTER TABLE `foodmenu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `queries`
--
ALTER TABLE `queries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `query_replies`
--
ALTER TABLE `query_replies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sports`
--
ALTER TABLE `sports`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `foodmenu`
--
ALTER TABLE `foodmenu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `queries`
--
ALTER TABLE `queries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `query_replies`
--
ALTER TABLE `query_replies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `sports`
--
ALTER TABLE `sports`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
