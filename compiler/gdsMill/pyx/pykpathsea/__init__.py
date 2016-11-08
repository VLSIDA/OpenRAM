# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2003-2004 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2003-2004 André Wobst <wobsta@users.sourceforge.net>
#
# This file is part of PyX (http://pyx.sourceforge.net/).
#
# PyX is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyX; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA


try:
    from _pykpathsea import * 
except:
    import os
    find_file_cache = {}
    def find_file(filename, kpse_file_format):
        command = 'kpsewhich --format="%s" %s' % (kpse_file_format, filename)
        if not find_file_cache.has_key(command):
            find_file_cache[command] = os.popen(command, "r").readline().strip()
        return find_file_cache[command]
    kpse_gf_format = "gf"
    kpse_pk_format = "pk"
    kpse_any_glyph_format = "bitmap font"
    kpse_tfm_format = "tfm"
    kpse_afm_format = "afm"
    kpse_base_format = "base"
    kpse_bib_format = "bib"
    kpse_bst_format = "bst"
    kpse_cnf_format = "cnf"
    kpse_db_format = "ls-R"
    kpse_fmt_format = "fmt"
    kpse_fontmap_format = "map"
    kpse_mem_format = "mem"
    kpse_mf_format = "mf"
    kpse_mfpool_format = "mfpool"
    kpse_mft_format = "mft"
    kpse_mp_format = "mp"
    kpse_mppool_format = "mppool"
    kpse_mpsupport_format = "MetaPost support"
    kpse_ocp_format = "ocp"
    kpse_ofm_format = "ofm"
    kpse_opl_format = "opl"
    kpse_otp_format = "otp"
    kpse_ovf_format = "ovf"
    kpse_ovp_format = "ovp"
    kpse_pict_format = "graphics/figure"
    kpse_tex_format = "tex"
    kpse_texdoc_format = "TeX system documentation"
    kpse_texpool_format = "texpool"
    kpse_texsource_format = "TeX system sources"
    kpse_tex_ps_header_format = "PostScript header"
    kpse_troff_font_format = "Troff fonts"
    kpse_type1_format = "type1 fonts"
    kpse_vf_format = "vf"
    kpse_dvips_config_format = "dvips config"
    kpse_ist_format = "ist"
    kpse_truetype_format = "truetype fonts"
    kpse_type42_format = "type42 fonts"
    kpse_web2c_format = "web2c"
    kpse_program_text_format = "other text files"
    kpse_program_binary_format = "other binary files"
    kpse_miscfonts_format = "misc fonts"
    kpse_web_format = "web"
    kpse_cweb_format = "cweb"
