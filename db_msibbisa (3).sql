-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 21, 2022 at 09:57 PM
-- Server version: 10.4.16-MariaDB
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_msibbisa`
--

-- --------------------------------------------------------

--
-- Table structure for table `absensi`
--

CREATE TABLE `absensi` (
  `pertemuan_ke` int(255) NOT NULL,
  `id_course` int(255) NOT NULL,
  `id_mahasiswa` int(255) NOT NULL,
  `keterangan` int(11) NOT NULL DEFAULT 11 COMMENT '11 Hadir, 22 Sakit, 33 Izin, 44 Aplha',
  `tanggal` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(255) NOT NULL,
  `username` varchar(255) CHARACTER SET latin1 NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `status_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `username`, `password`, `nama`, `status_id`) VALUES
(2, 'arityo451', 'd40f929d7bf7a283f82a648561231891', 'Ari Budi ppp', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `anggota_project`
--

CREATE TABLE `anggota_project` (
  `id_mahasiswa` int(11) NOT NULL,
  `id_posisi` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `id_course` int(255) NOT NULL,
  `nama_course` varchar(255) NOT NULL,
  `jam` int(255) NOT NULL,
  `kelas` varchar(255) NOT NULL,
  `jadwal` date NOT NULL,
  `id_admin` int(255) DEFAULT NULL,
  `limit` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `id_mahasiswa` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `nama_mahasiswa` varchar(255) NOT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `asal_kampus` varchar(255) NOT NULL,
  `posisi` varchar(255) NOT NULL,
  `id_admin` int(255) DEFAULT NULL,
  `foto_user` varchar(255) DEFAULT NULL,
  `status_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`id_mahasiswa`, `email`, `nama_mahasiswa`, `tanggal_lahir`, `password`, `asal_kampus`, `posisi`, `id_admin`, `foto_user`, `status_id`) VALUES
(9, 'ari.tyo52@gmail.com', 'Ari Budi P', NULL, '57082344f8ca880409ab44157180ba57', 'Universitas Amikom Purwokerto', 'AI Hacker', 2, NULL, 'mahasiswa');

-- --------------------------------------------------------

--
-- Table structure for table `mentor`
--

CREATE TABLE `mentor` (
  `id_mentor` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `nama_mentor` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `id_admin` int(255) DEFAULT NULL,
  `status_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mentor`
--

INSERT INTO `mentor` (`id_mentor`, `email`, `nama_mentor`, `password`, `id_admin`, `status_id`) VALUES
(7, 'ari.tyo52@gmail.com', 'Ari Budi P', '57082344f8ca880409ab44157180ba57', 2, 'mentor');

-- --------------------------------------------------------

--
-- Table structure for table `mentor_project`
--

CREATE TABLE `mentor_project` (
  `id_mentor` int(255) NOT NULL,
  `id_project` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `mom`
--

CREATE TABLE `mom` (
  `id_mom` int(255) NOT NULL,
  `id_mahasiswa` int(255) DEFAULT NULL,
  `id_project` int(255) DEFAULT NULL,
  `id_mentor` int(255) NOT NULL,
  `tanggal` datetime(6) NOT NULL,
  `dokumen_upload` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `nilai_course`
--

CREATE TABLE `nilai_course` (
  `id_course` int(255) NOT NULL,
  `id_mahasiswa` int(255) NOT NULL,
  `nilai` decimal(65,0) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `pengajar`
--

CREATE TABLE `pengajar` (
  `id_pengajar` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `nama_pengajar` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `id_admin` int(255) DEFAULT NULL,
  `status_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pengajar`
--

INSERT INTO `pengajar` (`id_pengajar`, `email`, `nama_pengajar`, `password`, `id_admin`, `status_id`) VALUES
(6, 'ari.tyo52@gmail.com', 'Ari Budi P', '57082344f8ca880409ab44157180ba57', 2, 'pengajar');

-- --------------------------------------------------------

--
-- Table structure for table `posisi_project`
--

CREATE TABLE `posisi_project` (
  `id_posisi` int(255) NOT NULL,
  `id_project` int(255) NOT NULL,
  `nama_posisi` varchar(255) NOT NULL,
  `skema_posisi` varchar(255) NOT NULL,
  `status_diambil` int(255) NOT NULL DEFAULT 0 COMMENT '0 Belum diambil, 11 Sudah diambil',
  `jumlah_dibuka` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

CREATE TABLE `project` (
  `id_project` int(255) NOT NULL,
  `nama_project` varchar(255) NOT NULL,
  `deskripsi` varchar(255) NOT NULL,
  `jadwal_mentoring` date NOT NULL,
  `jam` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `rppi`
--

CREATE TABLE `rppi` (
  `id_project` int(255) NOT NULL,
  `id_mahasiswa` int(255) NOT NULL,
  `jabatan` varchar(255) NOT NULL,
  `skema` varchar(255) NOT NULL,
  `status_verifikasi` int(11) NOT NULL DEFAULT 0 COMMENT '0 Belum verifikasi, 11 Sudah di Verifikasi'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `rppm`
--

CREATE TABLE `rppm` (
  `id_sertifikat` int(255) NOT NULL,
  `id_mahasiswa` int(255) NOT NULL,
  `skema` varchar(255) NOT NULL,
  `status_verifikasi` int(11) NOT NULL DEFAULT 0 COMMENT '0 Belum verifikasi, 11 Sudah di Verifikasi'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `rppt`
--

CREATE TABLE `rppt` (
  `id_mahasiswa` int(255) NOT NULL,
  `id_course` int(255) NOT NULL,
  `skema` varchar(255) NOT NULL,
  `status_verifikasi` int(11) NOT NULL DEFAULT 0 COMMENT '0 Belum Di verifikasi, 11 Sudah diVerifikasi'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `rpptamu`
--

CREATE TABLE `rpptamu` (
  `id_rpptamu` int(255) NOT NULL,
  `id_mahasiswa` int(255) NOT NULL,
  `id_sertifikat` int(255) NOT NULL,
  `skema` varchar(255) NOT NULL,
  `status_verifikasi` int(11) NOT NULL DEFAULT 0 COMMENT '0 Belum di Verifikasi, 11 Sudah di Verifikasi'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sertifikat`
--

CREATE TABLE `sertifikat` (
  `id_sertifikat` int(255) NOT NULL,
  `nama_sertifikat` varchar(255) NOT NULL,
  `upload_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absensi`
--
ALTER TABLE `absensi`
  ADD PRIMARY KEY (`pertemuan_ke`),
  ADD KEY `id_course` (`id_course`),
  ADD KEY `id_mahasiswa` (`id_mahasiswa`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`) USING BTREE,
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `anggota_project`
--
ALTER TABLE `anggota_project`
  ADD KEY `id_mahasiswa` (`id_mahasiswa`),
  ADD KEY `id_posisi` (`id_posisi`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`id_course`);

--
-- Indexes for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`id_mahasiswa`),
  ADD KEY `idx_admin` (`id_admin`);

--
-- Indexes for table `mentor`
--
ALTER TABLE `mentor`
  ADD PRIMARY KEY (`id_mentor`),
  ADD KEY `idx_admin` (`id_admin`);

--
-- Indexes for table `mentor_project`
--
ALTER TABLE `mentor_project`
  ADD KEY `id_mentor` (`id_mentor`),
  ADD KEY `id_project` (`id_project`);

--
-- Indexes for table `mom`
--
ALTER TABLE `mom`
  ADD PRIMARY KEY (`id_mom`),
  ADD KEY `id_mahasiswa` (`id_mahasiswa`),
  ADD KEY `id_mentor` (`id_mentor`),
  ADD KEY `id_project` (`id_project`);

--
-- Indexes for table `nilai_course`
--
ALTER TABLE `nilai_course`
  ADD KEY `id_course` (`id_course`),
  ADD KEY `id_mahasiswa` (`id_mahasiswa`);

--
-- Indexes for table `pengajar`
--
ALTER TABLE `pengajar`
  ADD PRIMARY KEY (`id_pengajar`),
  ADD KEY `idx_admin` (`id_admin`);

--
-- Indexes for table `posisi_project`
--
ALTER TABLE `posisi_project`
  ADD PRIMARY KEY (`id_posisi`),
  ADD KEY `id_project` (`id_project`);

--
-- Indexes for table `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`id_project`);

--
-- Indexes for table `rppi`
--
ALTER TABLE `rppi`
  ADD KEY `id_mahasiswa` (`id_mahasiswa`),
  ADD KEY `id_project` (`id_project`);

--
-- Indexes for table `rppm`
--
ALTER TABLE `rppm`
  ADD PRIMARY KEY (`id_sertifikat`),
  ADD KEY `idx_sertifikat` (`id_sertifikat`),
  ADD KEY `idx_mahasiswa` (`id_mahasiswa`);

--
-- Indexes for table `rppt`
--
ALTER TABLE `rppt`
  ADD KEY `idx_mahasiswa` (`id_mahasiswa`),
  ADD KEY `idx_course` (`id_course`);

--
-- Indexes for table `rpptamu`
--
ALTER TABLE `rpptamu`
  ADD PRIMARY KEY (`id_rpptamu`,`id_sertifikat`),
  ADD KEY `idx_sertifikat` (`id_sertifikat`),
  ADD KEY `idx_mahasiswa` (`id_mahasiswa`);

--
-- Indexes for table `sertifikat`
--
ALTER TABLE `sertifikat`
  ADD PRIMARY KEY (`id_sertifikat`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `absensi`
--
ALTER TABLE `absensi`
  MODIFY `pertemuan_ke` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `course`
--
ALTER TABLE `course`
  MODIFY `id_course` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  MODIFY `id_mahasiswa` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `mentor`
--
ALTER TABLE `mentor`
  MODIFY `id_mentor` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `mom`
--
ALTER TABLE `mom`
  MODIFY `id_mom` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pengajar`
--
ALTER TABLE `pengajar`
  MODIFY `id_pengajar` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `posisi_project`
--
ALTER TABLE `posisi_project`
  MODIFY `id_posisi` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `project`
--
ALTER TABLE `project`
  MODIFY `id_project` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `rpptamu`
--
ALTER TABLE `rpptamu`
  MODIFY `id_rpptamu` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sertifikat`
--
ALTER TABLE `sertifikat`
  MODIFY `id_sertifikat` int(255) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `absensi`
--
ALTER TABLE `absensi`
  ADD CONSTRAINT `absensi_ibfk_1` FOREIGN KEY (`id_course`) REFERENCES `course` (`id_course`),
  ADD CONSTRAINT `absensi_ibfk_2` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`);

--
-- Constraints for table `anggota_project`
--
ALTER TABLE `anggota_project`
  ADD CONSTRAINT `anggota_project_ibfk_1` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`),
  ADD CONSTRAINT `anggota_project_ibfk_2` FOREIGN KEY (`id_posisi`) REFERENCES `posisi_project` (`id_posisi`);

--
-- Constraints for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD CONSTRAINT `mahasiswa_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`);

--
-- Constraints for table `mentor`
--
ALTER TABLE `mentor`
  ADD CONSTRAINT `mentor_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`);

--
-- Constraints for table `mentor_project`
--
ALTER TABLE `mentor_project`
  ADD CONSTRAINT `mentor_project_ibfk_1` FOREIGN KEY (`id_mentor`) REFERENCES `mentor` (`id_mentor`),
  ADD CONSTRAINT `mentor_project_ibfk_2` FOREIGN KEY (`id_project`) REFERENCES `project` (`id_project`);

--
-- Constraints for table `mom`
--
ALTER TABLE `mom`
  ADD CONSTRAINT `mom_ibfk_1` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`),
  ADD CONSTRAINT `mom_ibfk_2` FOREIGN KEY (`id_mentor`) REFERENCES `mentor` (`id_mentor`),
  ADD CONSTRAINT `mom_ibfk_3` FOREIGN KEY (`id_project`) REFERENCES `project` (`id_project`);

--
-- Constraints for table `nilai_course`
--
ALTER TABLE `nilai_course`
  ADD CONSTRAINT `nilai_course_ibfk_1` FOREIGN KEY (`id_course`) REFERENCES `course` (`id_course`),
  ADD CONSTRAINT `nilai_course_ibfk_2` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`);

--
-- Constraints for table `pengajar`
--
ALTER TABLE `pengajar`
  ADD CONSTRAINT `pengajar_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`);

--
-- Constraints for table `posisi_project`
--
ALTER TABLE `posisi_project`
  ADD CONSTRAINT `posisi_project_ibfk_1` FOREIGN KEY (`id_project`) REFERENCES `project` (`id_project`);

--
-- Constraints for table `rppi`
--
ALTER TABLE `rppi`
  ADD CONSTRAINT `rppi_ibfk_1` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`),
  ADD CONSTRAINT `rppi_ibfk_2` FOREIGN KEY (`id_project`) REFERENCES `project` (`id_project`);

--
-- Constraints for table `rppm`
--
ALTER TABLE `rppm`
  ADD CONSTRAINT `rppm_ibfk_1` FOREIGN KEY (`id_sertifikat`) REFERENCES `sertifikat` (`id_sertifikat`),
  ADD CONSTRAINT `rppm_ibfk_2` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`);

--
-- Constraints for table `rppt`
--
ALTER TABLE `rppt`
  ADD CONSTRAINT `rppt_ibfk_1` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`),
  ADD CONSTRAINT `rppt_ibfk_2` FOREIGN KEY (`id_course`) REFERENCES `course` (`id_course`);

--
-- Constraints for table `rpptamu`
--
ALTER TABLE `rpptamu`
  ADD CONSTRAINT `rpptamu_ibfk_1` FOREIGN KEY (`id_sertifikat`) REFERENCES `sertifikat` (`id_sertifikat`),
  ADD CONSTRAINT `rpptamu_ibfk_2` FOREIGN KEY (`id_mahasiswa`) REFERENCES `mahasiswa` (`id_mahasiswa`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
