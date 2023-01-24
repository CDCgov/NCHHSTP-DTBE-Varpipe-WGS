import unittest
import os
import shutil
from clockwork import mykrobe, utils

modules_dir = os.path.dirname(os.path.abspath(mykrobe.__file__))
data_dir = os.path.join(modules_dir, "tests", "data", "mykrobe")


class TestMykrobe(unittest.TestCase):
    def test_run_predict_and_check_susceptibility(self):
        """test run_predict and susceptibility_dict_from_json_file"""
        reads_file = os.path.join(data_dir, "run_predict.reads.fq.gz")
        tmp_out = "tmp.mykrobe_run_predict"
        mykrobe.run_predict([reads_file], tmp_out, "sample_name", "tb")
        json_file = os.path.join(tmp_out, "out.json")
        suscept_data = mykrobe.susceptibility_dict_from_json_file(json_file)
        for drug in suscept_data:
            if drug == "Isoniazid":
                self.assertEqual("R", suscept_data[drug]["predict"])
            else:
                self.assertEqual("S", suscept_data[drug]["predict"])
        shutil.rmtree(tmp_out)

    def test_run_predict_and_check_susceptibility_custom_panel(self):
        """test run_predict and susceptibility_dict_from_json_file with custom panel"""
        # rerun the prvious test, but with custom probe and js on file. These just have the
        # embB_D328Y muatation. Should be susceptible
        reads_file = os.path.join(data_dir, "run_predict.reads.fq.gz")
        tmp_out = "tmp.mykrobe_run_predict"
        custom_probe = os.path.join(data_dir, "run_predict.probes.fa")
        custom_json = os.path.join(data_dir, "run_predict.json")
        mykrobe.run_predict(
            [reads_file, reads_file],
            tmp_out,
            "sample_name",
            "tb",
            custom_probe_and_json=(custom_probe, custom_json),
        )
        json_file = os.path.join(tmp_out, "out.json")
        suscept_data = mykrobe.susceptibility_dict_from_json_file(json_file)
        for drug in suscept_data:
            if drug == "Ethambutol":
                self.assertEqual("S", suscept_data[drug]["predict"])
            else:
                self.assertEqual("N", suscept_data[drug]["predict"])
        shutil.rmtree(tmp_out)

    def test_run_predict_and_check_susceptibility_fake_run_resistant(self):
        """test run_predict and susceptibility_dict_from_json_file in unittest mode with resistant call"""
        reads_file = os.path.join(data_dir, "run_predict.reads.fq.gz")
        tmp_out = "tmp.mykrobe_run_predict"
        mykrobe.run_predict(
            [reads_file],
            tmp_out,
            "sample_name",
            "tb",
            unittest=True,
            unittest_resistant=True,
        )
        json_file = os.path.join(tmp_out, "out.json")
        suscept_data = mykrobe.susceptibility_dict_from_json_file(json_file)
        for drug in suscept_data:
            if drug == "Isoniazid":
                self.assertEqual("R", suscept_data[drug]["predict"])
            else:
                self.assertEqual("S", suscept_data[drug]["predict"])
        shutil.rmtree(tmp_out)

    def test_run_predict_and_check_susceptibility_fake_run_susceptible(self):
        """test run_predict and susceptibility_dict_from_json_file in unittest mode with no resistant calls"""
        reads_file = os.path.join(data_dir, "run_predict.reads.fq.gz")
        tmp_out = "tmp.mykrobe_run_predict"
        mykrobe.run_predict(
            [reads_file],
            tmp_out,
            "sample_name",
            "tb",
            unittest=True,
            unittest_resistant=False,
        )
        json_file = os.path.join(tmp_out, "out.json")
        suscept_data = mykrobe.susceptibility_dict_from_json_file(json_file)
        for drug in suscept_data:
            self.assertEqual("S", suscept_data[drug]["predict"])
        shutil.rmtree(tmp_out)

    def test_panel_not_built_in(self):
        """test Panel not built-in"""
        species = "tb"
        name = "panel_name"
        panel_dir = "tmp.mykrobe.panel"
        custom_probe = os.path.join(data_dir, "run_predict.probes.fa")
        custom_json = os.path.join(data_dir, "run_predict.json")
        panel = mykrobe.Panel(panel_dir)
        panel.setup_files(species, name, custom_probe, custom_json)
        self.assertTrue(os.path.exists(panel.probes_fasta))
        self.assertTrue(os.path.exists(panel.var_to_res_json))
        self.assertEqual(species, panel.metadata["species"])
        self.assertEqual(name, panel.metadata["name"])
        self.assertFalse(panel.metadata["is_built_in"])
        shutil.rmtree(panel_dir)

    def test_panel_built_in(self):
        """test Panel built-in"""
        species = "tb"
        name = "walker-2015"
        panel_dir = "tmp.mykrobe.panel"
        panel = mykrobe.Panel(panel_dir)
        panel.setup_files(species, name, None, None)
        self.assertEqual(species, panel.metadata["species"])
        self.assertEqual(name, panel.metadata["name"])
        self.assertTrue(panel.metadata["is_built_in"])
        shutil.rmtree(panel_dir)
