from .jung.stacks import GrantStackType
from .mbti.types import MBTIType

def grant_type_to_mbti(grant_type: GrantStackType) -> MBTIType:
    return {
        GrantStackType.NiTeFiSe: MBTIType.INTJ,
        GrantStackType.TiNeSiFe: MBTIType.INTP,
        GrantStackType.TeNiSeFi: MBTIType.ENTJ,
        GrantStackType.NeTiFeSi: MBTIType.ENTP,
        GrantStackType.NiFeTiSe: MBTIType.INFJ,
        GrantStackType.FiNeSiTe: MBTIType.INFP,
        GrantStackType.FeNiSeTi: MBTIType.ENFJ,
        GrantStackType.NeFiTeSi: MBTIType.ENFP,
        GrantStackType.SiTeFiNe: MBTIType.ISTJ,
        GrantStackType.SiFeTiNe: MBTIType.ISFJ,
        GrantStackType.TeSiNeFi: MBTIType.ESTJ,
        GrantStackType.FeSiNeTi: MBTIType.ESFJ,
        GrantStackType.TiSeNiFe: MBTIType.ISTP,
        GrantStackType.FiSeNiTe: MBTIType.ISFP,
        GrantStackType.SeTiFeNi: MBTIType.ESTP,
        GrantStackType.SeFiTeNi: MBTIType.ESFP,
    }[grant_type]




def mbti_to_grant_type(mbti_type: MBTIType) -> GrantStackType:
    return {
        MBTIType.INTJ: GrantStackType.NiTeFiSe,
        MBTIType.INTP: GrantStackType.TiNeSiFe,
        MBTIType.ENTJ: GrantStackType.TeNiSeFi,
        MBTIType.ENTP: GrantStackType.NeTiFeSi,
        MBTIType.INFJ: GrantStackType.NiFeTiSe,
        MBTIType.INFP: GrantStackType.FiNeSiTe,
        MBTIType.ENFJ: GrantStackType.FeNiSeTi,
        MBTIType.ENFP: GrantStackType.NeFiTeSi,
        MBTIType.ISTJ: GrantStackType.SiTeFiNe,
        MBTIType.ISFJ: GrantStackType.SiFeTiNe,
        MBTIType.ESTJ: GrantStackType.TeSiNeFi,
        MBTIType.ESFJ: GrantStackType.FeSiNeTi,
        MBTIType.ISTP: GrantStackType.TiSeNiFe,
        MBTIType.ISFP: GrantStackType.FiSeNiTe,
        MBTIType.ESTP: GrantStackType.SeTiFeNi,
        MBTIType.ESFP: GrantStackType.SeFiTeNi,
    }[mbti_type]

