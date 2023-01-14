from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/advanced_depends"
)


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, text: str = ""):
        return self
        if text:
            return self.fixed_content in text
        return False


checker = FixedContentQueryChecker("bar")


@router.get("/query-checker/")
async def read_query_check(fixed_content_included = Depends(checker)):
    return {"fixed_content_in_query": id(fixed_content_included)}

