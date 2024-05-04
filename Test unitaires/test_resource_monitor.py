import unittest
from unittest.mock import patch
import io
import sys


from resource_monitor import check_resources

class TestResourceMonitor(unittest.TestCase):
    
    # Test du seuil par défaut
    def test_default_threshold(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            check_resources()
            output = fake_stdout.getvalue().strip()
            self.assertEqual(output, "")

    # Test du seuil personnalisé
    def test_custom_threshold(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            check_resources(70)
            output = fake_stdout.getvalue().strip()
            self.assertEqual(output, "")

    # Test du cas où tous les seuils sont dépassés
    def test_all_thresholds_exceeded(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            check_resources(50)
            output = fake_stdout.getvalue().strip()
            self.assertIn("CPU usage is", output)
            self.assertIn("Memory usage is", output)
            self.assertIn("Disk usage is", output)

    # Test du cas où aucun seuil n'est dépassé
    def test_no_threshold_exceeded(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            check_resources(90)
            output = fake_stdout.getvalue().strip()
            self.assertEqual(output, "")

    # Test du cas où seule une ressource dépasse le seuil
    def test_single_threshold_exceeded(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            check_resources(80)
            output = fake_stdout.getvalue().strip()
            self.assertIn("CPU usage is", output)
            self.assertNotIn("Memory usage is", output)
            self.assertNotIn("Disk usage is", output)

    # Test de la gestion des erreurs
    @patch('psutil.cpu_percent', side_effect=Exception)
    @patch('psutil.virtual_memory', side_effect=Exception)
    @patch('psutil.disk_usage', side_effect=Exception)
    def test_error_handling(self, mock_cpu_percent, mock_virtual_memory, mock_disk_usage):
        with self.assertRaises(Exception):
            check_resources()

    # Test de la fonction avec des seuils invalides
    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            check_resources(-1)

if __name__ == '__main__':
    unittest.main()
