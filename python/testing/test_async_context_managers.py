from asynctest import CoroutineMock, TestCase, MagicMock


class ContextManager:

    async def __aenter__(self) -> "ContextManager":
        """Original enter method to be mocked out"""
        return self

    async def say_hello(self):
        return "hello"

    async def __aexit__(self, exc_type, exc, tb):
        """Original exit method to be mocked out"""
        pass


class UnitUnderTest:

    def __init__(self):
        self.context_manager: ContextManager = ContextManager()

    async def test_me(self):
        async with self.context_manager as cm:
            return await cm.say_hello()


class TestAsyncContextManager(TestCase):

    def setUp(self):
        self.uut = UnitUnderTest()

    async def test_context_manager(self):
        """Test without mocking"""
        self.assertEqual(await self.uut.test_me(), "hello")

    async def test_context_manager_mocked(self):
        """Test with the context manager mocked out"""
        mock = MagicMock()

        context = CoroutineMock()
        context.say_hello = CoroutineMock(return_value="mocked!")
        
        mock.__aenter__ = CoroutineMock(return_value=context)
        mock.__aexit__ = CoroutineMock()
        
        self.uut.context_manager = mock
        self.assertEqual(await self.uut.test_me(), "mocked!")
