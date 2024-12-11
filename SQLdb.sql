--
-- Tabellstruktur for tabell `channel`
--

CREATE TABLE `channel` (
  `id` varchar(25) NOT NULL,
  `name` varchar(50) NOT NULL,
  `tag_name` varchar(50) NOT NULL,
  `tag_id` varchar(25) NOT NULL,
  `join_limit` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `raids`
--

CREATE TABLE `raids` (
  `id` int(11) NOT NULL,
  `host_id` varchar(25) NOT NULL,
  `host_tc` varchar(25) NOT NULL,
  `host_username` varchar(50) NOT NULL,
  `pokemon_id` varchar(10) NOT NULL,
  `pokemon_name` varchar(50) NOT NULL,
  `pokemon_img` varchar(255) NOT NULL,
  `cp_unboosted` varchar(4) NOT NULL,
  `cp_boosted` varchar(4) NOT NULL,
  `type` varchar(25) NOT NULL,
  `channel_id` varchar(25) NOT NULL,
  `channel_tag` varchar(25) NOT NULL,
  `channel_limit` varchar(15) NOT NULL,
  `msg_id` varchar(25) NOT NULL,
  `tag_id` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `stats`
--

CREATE TABLE `stats` (
  `id` int(10) NOT NULL,
  `channel` varchar(50) NOT NULL,
  `user` varchar(50) NOT NULL,
  `pokemon` varchar(50) NOT NULL,
  `raid_started` varchar(1) NOT NULL,
  `date` varchar(100) NOT NULL,
  `raid_id` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `users`
--

CREATE TABLE `users` (
  `id` varchar(25) NOT NULL,
  `username` varchar(50) NOT NULL,
  `ingame_name` varchar(50) NOT NULL,
  `trainer_code` varchar(50) NOT NULL,
  `level` varchar(2) NOT NULL,
  `country` varchar(50) NOT NULL,
  `team` varchar(50) NOT NULL,
  `raids_joined` int(10) NOT NULL,
  `raids_hosted` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `channel`
--
ALTER TABLE `channel`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `raids`
--
ALTER TABLE `raids`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stats`
--
ALTER TABLE `stats`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `raids`
--
ALTER TABLE `raids`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `stats`
--
ALTER TABLE `stats`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
