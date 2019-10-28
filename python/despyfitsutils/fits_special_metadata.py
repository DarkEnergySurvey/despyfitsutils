# $Id: special_metadata_funcs.py 38203 2015-05-17 14:28:09Z mgower $
# $Rev:: 38203                            $:  # Revision of last commit.
# $LastChangedBy:: mgower                 $:  # Author of last commit.
# $LastChangedDate:: 2015-05-17 09:28:09 #$:  # Date of last commit.

"""
    Specialized functions for computing metadata
"""

import pyfits
import despyfitsutils.fitsutils as fitsutils
import despymisc.create_special_metadata as spmeta


######################################################################
# !!!! Function name must be all lowercase
# !!!! Function name must be of pattern func_<header key>
######################################################################


######################################################################
def func_band(filename, hdulist=None, whichhdu=None):
    """ Create band from the 'FILTER' keyword

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        str
            Contains the value of the 'FILTER' keyword.
    """

    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    filterval = fitsutils.get_hdr_value(hdulist2, 'FILTER', whichhdu)

    if hdulist is None:
        hdulist2.close()

    return spmeta.create_band(filterval)


######################################################################
def func_camsym(filename, hdulist=None, whichhdu=None):
    """ Create camsym from the 'INSTRUME' keyword value.

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        str
            Contains the generated camsym.

    """
    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    instrume = fitsutils.get_hdr_value(hdulist2, 'INSTRUME', whichhdu)

    if hdulist is None:
        hdulist2.close()

    return spmeta.create_camsym(instrume)


######################################################################
def func_nite(filename, hdulist=None, whichhdu=None):
    """ Create nite from the 'DATE-OBS' keyword value.

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        str
            Contains the generated nite.

    """

    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    date_obs = fitsutils.get_hdr_value(hdulist2, 'DATE-OBS', whichhdu)

    if hdulist is None:
        hdulist2.close()

    return spmeta.create_nite(date_obs)


######################################################################
def func_objects(filename, hdulist=None, whichhdu=None):
    """ return the number of objects in a FITS catalog, which is assumed
        to be the value of the 'NAXIS2' keyword.

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        int
            The number of objects in the catalog.

    """
    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    objects = fitsutils.get_hdr_value(hdulist2, 'NAXIS2', whichhdu)

    if hdulist is None:
        hdulist2.close()

    return objects


######################################################################
def func_field(filename, hdulist=None, whichhdu=None):
    """ Get the field from the 'OBJECT' FITS header value

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        str
            Contains the generated field value.

    """
    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    try:
        objectval = fitsutils.get_hdr_value(hdulist2, 'OBJECT', whichhdu)
    except:
        objectval = fitsutils.get_hdr_value(hdulist2, 'OBJECT', 'LDAC_IMHEAD')

    if hdulist is None:
        hdulist2.close()

    return spmeta.create_field(objectval)

######################################################################
def func_radeg(filename, hdulist=None, whichhdu=None):
    """ Get the FITS header value of 'RA' in decimal degrees.

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        float
            The decimal value of the RA.
    """
    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    ra = fitsutils.get_hdr_value(hdulist2, 'RA', whichhdu)

    if hdulist is None:
        hdulist2.close()

    return spmeta.convert_ra_to_deg(ra)

######################################################################
def func_tradeg(filename, hdulist=None):
    """ Get the FITS header value of 'TELRA' in degrees

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        float
            The value of TELRA in decimal degrees.
    """
    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    telra = fitsutils.get_hdr_value(hdulist2, 'TELRA')

    if hdulist is None:
        hdulist2.close()

    return spmeta.convert_ra_to_deg(telra)

######################################################################
def func_decdeg(filename, hdulist=None, whichhdu=None):
    """ Get the FITS header value of 'DEC' in degrees

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        float
            The value of DEC in decimal degrees.

    """
    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    dec = fitsutils.get_hdr_value(hdulist2, 'DEC', whichhdu)

    if hdulist is None:
        hdulist2.close()

    return spmeta.convert_dec_to_deg(dec)

######################################################################
def func_tdecdeg(filename, hdulist=None):
    """ Get the fits header value 'TELDEC' in degrees

        Parameters
        ----------
        filename : str
            The file to get the filter keyword from (must be a fits file),
            only used if hdulist is ``None``.

        hdulist : astropy.io.fits.HDUList, optional
            A listing of the HDUs to search for the requested HDU,
            default is ``None``, in which case `filename` is opened and used.

        whichhdu : various, optional
            The HDU being searched for, this can be an int for the HDU index,
            a string for the HDU name, or ``None`` in which case the primary
            HDU is used. The default is ``None``.

        Returns
        -------
        float
            The value of TELDEC in decimal degrees.

    """
    hdulist2 = None
    if hdulist is None:
        hdulist2 = pyfits.open(filename, 'readonly')
    else:
        hdulist2 = hdulist

    teldec = fitsutils.get_hdr_value(hdulist2, 'TELDEC')

    if hdulist is None:
        hdulist2.close()

    return spmeta.convert_dec_to_deg(teldec)
