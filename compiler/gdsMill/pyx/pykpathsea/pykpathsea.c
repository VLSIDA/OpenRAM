/*  pykpathsea.c: Copyright 2003 Jörg Lehmann, André Wobst
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
 *  USA.
 */

#include <Python.h>
#include <kpathsea/tex-file.h>
#include <kpathsea/progname.h>

static PyObject *py_kpse_find_file(PyObject *self, PyObject *args)
{
  char *filename;
  int kpse_file_format;
  char *completefilename;
  PyObject *returnvalue;

  if (PyArg_ParseTuple(args, "si", &filename, &kpse_file_format)) {
    completefilename = kpse_find_file(filename, (kpse_file_format_type) kpse_file_format, 1);

    returnvalue = Py_BuildValue("s", completefilename);
    /* XXX: free(completefilename); */
    return returnvalue;
  }

  return NULL;

}

/* exported methods */

static PyMethodDef pykpathsea_methods[] = {
  {"find_file", py_kpse_find_file,  METH_VARARGS},
  {NULL, NULL}
};

#define AddInt(x) PyDict_SetItemString(dict, #x, PyInt_FromLong(x))

void init_pykpathsea(void)
{
  PyObject *module = Py_InitModule("_pykpathsea", pykpathsea_methods);
  PyObject *dict = PyModule_GetDict(module);
  kpse_set_program_name("dvips", "dvips");

  AddInt(kpse_gf_format);
  AddInt(kpse_pk_format);
  AddInt(kpse_any_glyph_format);
  AddInt(kpse_tfm_format);
  AddInt(kpse_afm_format);
  AddInt(kpse_base_format);
  AddInt(kpse_bib_format);
  AddInt(kpse_bst_format);
  AddInt(kpse_cnf_format);
  AddInt(kpse_db_format);
  AddInt(kpse_fmt_format);
  AddInt(kpse_fontmap_format);
  AddInt(kpse_mem_format);
  AddInt(kpse_mf_format);
  AddInt(kpse_mfpool_format);
  AddInt(kpse_mft_format);
  AddInt(kpse_mp_format);
  AddInt(kpse_mppool_format);
  AddInt(kpse_mpsupport_format);
  AddInt(kpse_ocp_format);
  AddInt(kpse_ofm_format);
  AddInt(kpse_opl_format);
  AddInt(kpse_otp_format);
  AddInt(kpse_ovf_format);
  AddInt(kpse_ovp_format);
  AddInt(kpse_pict_format);
  AddInt(kpse_tex_format);
  AddInt(kpse_texdoc_format);
  AddInt(kpse_texpool_format);
  AddInt(kpse_texsource_format);
  AddInt(kpse_tex_ps_header_format);
  AddInt(kpse_troff_font_format);
  AddInt(kpse_type1_format);
  AddInt(kpse_vf_format);
  AddInt(kpse_dvips_config_format);
  AddInt(kpse_ist_format);
  AddInt(kpse_truetype_format);
  AddInt(kpse_type42_format);
  AddInt(kpse_web2c_format);
  AddInt(kpse_program_text_format);
  AddInt(kpse_program_binary_format);
  AddInt(kpse_miscfonts_format);
  /*
  AddInt(kpse_web_format);
  AddInt(kpse_cweb_format);
  */

}
